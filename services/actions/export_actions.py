import json
import time
from pathlib import Path
from threading import Thread

from core.contracts import ActionResult, ActionService
from db.repositories import UserRepository, SessionRepository
from shared.constants import EXPORT_DIR

def write_user_export_backup(data, export_path):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    export_path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


class UserExportAction(ActionService):
    def __init__(self, users: UserRepository | None = None):
        self.users = users or UserRepository()

    def execute(self, form, files, actor):
        users = self.users.list_all()
        data = [dict(row) for row in users]

        filename = f"user_export_backup_{int(time.time())}.json"
        export_path = EXPORT_DIR / filename

        Thread(
            target=write_user_export_backup,
            args=(data, export_path),
            daemon=True
        ).start()

        return ActionResult(
            "User export generated and backup started",
            {
                "file": filename,
                "path": str(export_path),
                "rows": len(data)
            }
        )


class SessionLookupAction(ActionService):
    def __init__(self, sessions: SessionRepository | None = None):
        self.sessions = sessions or SessionRepository()

    def execute(self, form, files, actor):
        return ActionResult(
            "Session checked",
            self.sessions.find_active(form.get("session_id", ""))
        )