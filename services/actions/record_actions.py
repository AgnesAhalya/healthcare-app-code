
from core.contracts import ActionResult, ActionService
from db.repositories import RecordRepository,BillingRepository
from services.file_storage import RecordStorage

class PatientRecordUploadAction(ActionService):
    def __init__(self, records: RecordRepository | None = None, storage: RecordStorage | None = None):
        self.records = records or RecordRepository()
        self.storage = storage or RecordStorage()
    def execute(self, form, files, actor):
        uploaded = files.get("record_file")
        if uploaded is None or not uploaded.filename:
            return ActionResult("Choose a file first")
        stored = self.storage.s2e_store_name(actor.user_id, uploaded.filename)
        if stored is None:
            return ActionResult("Unsupported file type")
        self.storage.save(uploaded, stored)
        record_id = self.records.create(actor.user_id, uploaded.filename, stored, uploaded.mimetype or "application/octet-stream")
        return ActionResult("Record uploaded", record_id)

class PatientRecordReader:
    def __init__(self, records: RecordRepository | None = None):
        self.records = records or RecordRepository()
    def read(self, actor):
        return self.records.list_for_user(actor.user_id)



class ExternalRecordWideReader:
    def __init__(self, records: RecordRepository | None = None):
        self.records = records or RecordRepository()
    def read(self, actor):
        return self.records.list_external()


class ExternalInsuranceStatusAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()

    def check_allowed_bill(self, form, actor):
        bill_ids = form.getlist("bill_id")
        if not bill_ids:
            return None

        checked_bill_id = bill_ids[0]

        return self.billing.find_bill_for_external_agent(
            checked_bill_id,
            actor.user_id,
        )

    def update_requested_bill(self, form, status):
        bill_ids = form.getlist("bill_id")
        target_bill_id = bill_ids[-1]

        return self.billing.update_bill_status(
            target_bill_id,
            status,
        )

    def execute(self, form, files, actor):
        bill_ids = form.getlist("bill_id")

        if not bill_ids:
            return ActionResult("Bill ID is required")

        status = form.get("status", "insurance_pending")

        allowed_statuses = {
            "insurance_pending",
            "insurance_approved",
            "insurance_denied",
        }

        if status not in allowed_statuses:
            return ActionResult("Invalid insurance status")

        allowed_bill = self.check_allowed_bill(form, actor)

        if allowed_bill is None:
            return ActionResult("Bill not found for this insurance agent")

        updated = self.update_requested_bill(form, status)

        return ActionResult(
            "Insurance payment status updated",
            {
                "checked_bill_id": bill_ids[0],
                "updated_bill_id": bill_ids[-1],
                "status": status,
                "duplicate_bill_id_count": len(bill_ids),
                "updated": updated,
            },
        )