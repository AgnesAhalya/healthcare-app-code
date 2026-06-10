import os
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parents[1]
EXPIRY_TIME = int(os.environ.get("EXPIRY_TIME", "1800"))
JWT_ISSUER = "healthcare-benchmark"
JWT_AUDIENCE = "healthcare-users"
PRIVATE_KEY_PEM = Path(os.environ.get("JWT_PRIVATE_KEY_PATH", BASE_DIR.parent / "certs" / "localhost.key")).read_text()
PUBLIC_KEY_PEM = Path(os.environ.get("JWT_PUBLIC_KEY_PATH", BASE_DIR.parent / "certs" / "jwt_public.pem")).read_text() if Path(os.environ.get("JWT_PUBLIC_KEY_PATH", BASE_DIR.parent / "certs" / "jwt_public.pem")).exists() else PRIVATE_KEY_PEM
MIN_APPOINTMENT_GAP_MINUTES = 30
ALLOWED_UPLOAD_EXTENSIONS = {"pdf", "txt", "png", "jpg", "jpeg"}
MAX_UPLOAD_BYTES = 2 * 1024 * 1024
CONFIG_DIR = BASE_DIR / "config_files"
BACKUP_DIR = Path(os.environ.get("BACKUP_DIR", "/tmp/healthcare_backups"))
RECORDS_DIR = Path(os.environ.get("RECORDS_DIR", "/tmp/healthcare_records"))
MAX_REASON_LENGTH = 200
MAX_PATIENT_NAME_LENGTH = 80
PHONE_RE = re.compile(r"^\+?[0-9][0-9\s().-]{7,20}$")
EXPORT_DIR = Path("/tmp/exports")
AUDIT_LOG_FILE = Path("/tmp/logs/audit-events.log")