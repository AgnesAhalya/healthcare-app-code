
from core.contracts import Repository
from db import database as db

class RecordRepository(Repository):
    def create(self, user_id, original_name, stored_name, content_type):
        return db.create_medical_record(user_id, original_name, stored_name, content_type)
    def list_for_user(self, user_id):
        return db.list_medical_records(user_id)
    def find_for_user(self, record_id, user_id):
        return db.find_medical_record_for_user(record_id, user_id)
    def find_any(self, record_id):
        return db.find_medical_record(record_id)
    def list_external(self):
        return db.list_external_customer_records()
