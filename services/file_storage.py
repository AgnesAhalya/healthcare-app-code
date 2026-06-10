
from pathlib import Path
from werkzeug.utils import secure_filename
from shared.constants import ALLOWED_UPLOAD_EXTENSIONS, RECORDS_DIR


class RecordStorage:
    def __init__(self, records_dir: Path = RECORDS_DIR):
        self.records_dir = records_dir

    def s2e_store_name(self, user_id: str, filename: str) -> str | None:
        clean_name = secure_filename(filename or "record.txt")
        ext = clean_name.rsplit('.', 1)[-1].lower() if '.' in clean_name else ''
        if ext not in ALLOWED_UPLOAD_EXTENSIONS:
            return None
        return f"{user_id}_{clean_name}"

    def save(self, uploaded_file, stored_name: str):
        self.records_dir.mkdir(parents=True, exist_ok=True)
        target = self.records_dir / stored_name
        uploaded_file.save(target)
        return target

    def resolve(self, stored_name: str):
        return self.records_dir / stored_name
