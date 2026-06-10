from db import database as db
from db.repositories import BillingRepository, UserRepository
from shared.constants import CONFIG_DIR

class StaticReader:
    def __init__(self, payload):
        self.payload = payload
    def read(self, actor):
        return self.payload


class LimitedRecordsReader:
    def read(self, actor):
        return db.list_all_records_limited()


class PaymentEntryReader:
    def read(self, actor):
        return db.list_payment_entries()


class PaymentHistoryReader:
    def __init__(self, billing: BillingRepository | None = None):
        self.billing = billing or BillingRepository()
    def read(self, actor):
        return self.billing.list_payments_for_user(actor.user_id)


class UserListReader:
    def __init__(self, users: UserRepository | None = None):
        self.users = users or UserRepository()
    def read(self, actor):
        return self.users.list_all()


class ConfigFileReader:
    def read(self, actor):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        files = []
        for p in sorted(CONFIG_DIR.glob("*")):
            if p.is_file():
                files.append({"name": p.name, "preview": p.read_text(errors="ignore")[:160]})
        return files
