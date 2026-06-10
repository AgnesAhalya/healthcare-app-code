
from core.contracts import ActionResult, ActionService
from db.repositories import ContentRepository
from shared.constants import BACKUP_DIR

class BackupSaveAction(ActionService):
    def execute(self, form, files, actor):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        path = BACKUP_DIR / form.get("name", "backup.txt")
        path.write_text(form.get("body", ""))
        return ActionResult("Backup saved", str(path))

class BackupRestoreAction(ActionService):
    def __init__(self, content: ContentRepository | None = None):
        self.content = content or ContentRepository()
    def execute(self, form, files, actor):
        uploaded = files.get("backup_file")
        raw = uploaded.read() if uploaded else b""
        return ActionResult("Backup restored", self.content.us2e_load_backup(raw))
