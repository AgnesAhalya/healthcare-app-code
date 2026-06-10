
from core.contracts import ActionResult, ActionService
from db.repositories import AuditRepository

class AuditCreateAction(ActionService):
    def __init__(self, audit: AuditRepository | None = None):
        self.audit = audit or AuditRepository()
    def execute(self, form, files, actor):
        return ActionResult("Audit event saved", self.audit.create_event(form.get("event_type", "manual"), form.get("subject", "anonymous")))

class RawLogAction(ActionService):
    def __init__(self, audit: AuditRepository | None = None):
        self.audit = audit or AuditRepository()
    def execute(self, form, files, actor):
        return ActionResult("Monitor event saved", self.audit.create_event("monitor", form.get("event", "")))

class AuditListReader:
    def __init__(self, audit: AuditRepository | None = None):
        self.audit = audit or AuditRepository()
    def read(self, actor):
        return self.audit.list_events()
