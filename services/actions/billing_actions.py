
from core.contracts import ActionResult, ActionService
from db.repositories import BillingRepository

class PatientBillPayAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        bill_id = form.get("bill_id", "")
        bill = self.billing.find_bill_for_user(bill_id, actor.user_id)
        if bill is None:
            return ActionResult("Bill not found")
        self.billing.mark_paid(bill_id, actor.user_id)
        return ActionResult("Payment complete", redirect_to=(form.get("return_to") or "/outpatient/bills"))

class ClientAmountPaymentAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        cents = int(float(form.get("amount", "0")) * 100)
        self.billing.create_payment(form.get("bill_id", ""), actor.user_id, cents, f"client-sig:{form.get('signature', '')}")
        return ActionResult("Client amount submitted")

class BillingEntryAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        payment_id = self.billing.create_payment(form.get("bill_id", ""), form.get("user_id", ""), form.get("amount_cents", "0"), form.get("note", ""))
        return ActionResult("Payment entered", payment_id)

class PatientBillReader:
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def read(self, actor):
        return self.billing.list_patient_bills(actor.user_id)

class AllBillReader:
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def read(self, actor):
        return self.billing.list_all_bills()
