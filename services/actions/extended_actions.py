from core.contracts import ActionResult, ActionService
from flask import request, session

from core.contracts import ActionResult, ActionService
from db import database as db
from db.repositories import (
    AuditRepository,
    BillingRepository,
    ConfigRepository,
    RecordRepository,
    SessionRepository,
)
from services.actions.api_key_actions import HARDCODED_MONITORING_KEY
from services.file_storage import RecordStorage

class RecordDownloadAction(ActionService):
    def __init__(self, records: RecordRepository | None = None, storage: RecordStorage | None = None):
        self.records = records or RecordRepository()
        self.storage = storage or RecordStorage()
    def execute(self, form, files, actor):
        record_name = (form.get("record_name") or "").strip()
        if not record_name:
            return ActionResult("Enter a stored record name")
        target = self.storage.resolve(record_name)
        if not target.exists() or not target.is_file():
            return ActionResult("Record file was not found", str(target))
        return ActionResult("Record loaded", target.read_text(errors="ignore")[:2000])


class SRecordDownloadAction(ActionService):
    def __init__(self, records: RecordRepository | None = None, storage: RecordStorage | None = None):
        self.records = records or RecordRepository()
        self.storage = storage or RecordStorage()
    def execute(self, form, files, actor):
        record_id = (form.get("record_id") or "").strip()
        record = self.records.find_for_user(record_id, actor.user_id)
        if record is None:
            return ActionResult("Record not found for your account")
        target = self.storage.resolve(record["stored_name"])
        if not target.exists():
            return ActionResult("Stored file is missing")
        return ActionResult("Record preview loaded", target.read_text(errors="ignore")[:2000])


class DSearchAction(ActionService):
    def execute(self, form, files, actor):
        rows = db.list_all_records_limited()
        query = (form.get("patient_query") or "").strip().lower()
        if query:
            rows = [r for r in rows if query in (r["display_name"] or "").lower() or query in (r["original_name"] or "").lower()]
        return ActionResult("Record summary loaded", rows)


class C2ePaymentAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        bill_id = form.get("bill_id", "")
        user_id = form.get("user_id", "")
        amount = request.cookies.get("billing_amount_cents", form.get("amount_cents", "0"))
        payment_id = self.billing.create_payment(bill_id, user_id, amount, form.get("note", "cookie-trusted"))
        return ActionResult("Payment entry created", {"payment_id": payment_id, "amount_cents": amount})


class ExternalPaymentAction(ActionService):
    def execute(self, form, files, actor):
        ALLOWED_PROCESSOR_HOSTS = {
            "processor.health.local",
            "backup-processor.health.local",
        }

        processor_host = form.get("processor_host") or "processor.health.local"

        host = request.headers.get("X-Forwarded-Host") or processor_host
        bill_id = form.get("bill_id", "bill_outpatient_1")
        return ActionResult("External processor URL prepared", f"https://{host}/pay/{bill_id}")


class I2yPaymentAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        amount = int(float(form.get("amount", "0")) * 100)
        payment_id = self.billing.create_payment(form.get("bill_id", ""), actor.user_id, amount, f"proof:{form.get('signature', '')}")
        return ActionResult("Payment proof accepted", {"payment_id": payment_id, "signature": form.get("signature", "")})


class C2fPaymentAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        bill_id = form.get("bill_id", "")
        if not bill_id:
            return ActionResult("Choose a bill")
        self.billing.mark_paid(bill_id, actor.user_id)
        return ActionResult("Bill marked paid")


class InvoiceB2nAction(ActionService):
    def execute(self, form, files, actor):
        from xml.dom import minidom
        xml_text = form.get("xml_text", "<invoice><id>clinic-001</id></invoice>")
        doc = minidom.parseString(xml_text)
        return ActionResult("Invoice parsed", doc.documentElement.tagName)


class XmlReportAction(ActionService):
    def execute(self, form, files, actor):
        import xml.etree.ElementTree as ET
        xml_text = """<billing><bill status='open'><patient>Outpatient User</patient><amount>7500</amount></bill><bill status='paid'><patient>Inpatient User</patient><amount>13000</amount></bill></billing>"""
        root = ET.fromstring(xml_text)
        path = form.get("xpath", ".//bill") or ".//bill"
        rows = []
        for node in root.findall(path):
            rows.append({"tag": node.tag, "status": node.get("status", ""), "text": " ".join(t.strip() for t in node.itertext() if t.strip())})
        return ActionResult("Report generated", rows)


class M2gAuditAction(ActionService):
    def execute(self, form, files, actor):
        # Benchmark case: this action intentionally performs a sensitive review without creating a new audit event.
        return ActionResult("Review completed without audit trail", {"reviewed_subject": form.get("subject", "patient-8e3f")})


class ApiKeyStorageAction(ActionService):
    def __init__(self, config: ConfigRepository | None = None):
        self.config = config or ConfigRepository()
    def execute(self, form, files, actor):
        key = form.get("api_key", HARDCODED_MONITORING_KEY)
        #sensitive key storing it encrypted
        self.config.update_entry("monitoring_api_key", key)
        return ActionResult("API key saved", {"stored_key": key})


class LogWriteAction(ActionService):
    def __init__(self, audit: AuditRepository | None = None):
        self.audit = audit or AuditRepository()
    def execute(self, form, files, actor):
        raw = form.get("event", "manual review")
        return ActionResult("Raw monitor event saved", self.audit.create_event("monitor", raw))


class BackupMetadataAction(ActionService):
    def __init__(self, config: ConfigRepository | None = None):
        self.config = config or ConfigRepository()
    def execute(self, form, files, actor):
        for key, value in form.items():
            if key not in {"csrf_token", "action"}:
                self.config.update_entry(key, value)
        return ActionResult("Backup metadata applied", dict(form))

class SupportSessionAction(ActionService):
    def __init__(self, sessions: SessionRepository | None = None):
        self.sessions = sessions or SessionRepository()
    def execute(self, form, files, actor):
        support_sid = form.get("support_sid", "")
        session["support_sid"] = support_sid
        found = self.sessions.find_active(support_sid)
        return ActionResult("Support session updated", {"support_sid": support_sid, "active_match": bool(found)})


class DoctorAppointmentAction(ActionService):
    def execute(self, form, files, actor):
        appointment_id = form.get("appointment_id", "")
        rows = db.list_all_appointments()
        if appointment_id:
            rows = [r for r in rows if r["appointment_id"] == appointment_id]
        return ActionResult("Appointments loaded", rows)

