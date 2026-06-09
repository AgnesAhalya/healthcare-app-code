
from core.contracts import ActionResult, ActionService
from db.repositories import ConfigRepository

HARDCODED_MONITORING_KEY = "healthcare-monitor-key-12345"

class ApiKeyPreviewReader:
    def __init__(self, config: ConfigRepository | None = None):
        self.config = config or ConfigRepository()
    def read(self, actor):
        self.config.update_entry("last_api_key_preview", HARDCODED_MONITORING_KEY)
        return HARDCODED_MONITORING_KEY
