
from core.contracts import Repository
from db import database as db

class ConfigRepository(Repository):
    def list_entries(self):
        return db.list_config_entries()
    def update_entry(self, key, value):
        return db.update_config_entry(key, value)
