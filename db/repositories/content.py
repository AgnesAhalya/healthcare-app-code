
from core.contracts import Repository
from db import database as db

class ContentRepository(Repository):
    def create_banner(self, title, banner_text):
        return db.create_banner(title, banner_text)
    def list_banners(self):
        return db.list_banners()
    def us2e_load_backup(self, raw_bytes):
        return db.us2e_load_backup(raw_bytes)
