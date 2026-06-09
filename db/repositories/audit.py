
from core.contracts import Repository
from db import database as db

import time
from shared.constants import AUDIT_LOG_FILE



class AuditRepository(Repository):
    def create_event(self, event_type, anonymized_subject):
        event_id = db.create_audit_event(event_type, anonymized_subject)

        AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with AUDIT_LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(
                f"{int(time.time())} event_id={event_id} "
                f"type={event_type} subject={anonymized_subject}\n"
            )

        return event_id

    def list_events(self):
        if not AUDIT_LOG_FILE.exists():
            return []

        rows = []

        for index, line in enumerate(AUDIT_LOG_FILE.read_text(errors="ignore").splitlines(), start=1):
            rows.append(
                {
                    "event_id": str(index),
                    "event_type": "file_log",
                    "anonymized_subject": line,
                }
            )

        return rows
