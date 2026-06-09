
from core.contracts import ActionResult, ActionService
from db.repositories import BillingRepository

class ReportQueryAction(ActionService):
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def execute(self, form, files, actor):
        return ActionResult("Report generated", self.billing.run_raw_report(form.get("where_clause")))
