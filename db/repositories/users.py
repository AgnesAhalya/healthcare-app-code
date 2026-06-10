
from core.contracts import Repository
from db import database as db

class UserRepository(Repository):
    def create_patient(self, username, password, user_type, display_name, phone):
        return db.create_patient_user(username, password, user_type, display_name, phone)
    def find_by_username(self, username):
        return db.find_user_by_username(username)
    def list_all(self):
        return db.list_users()
    def find_profile(self, user_id):
        return db.find_profile_by_user_id(user_id)
    def update_profile(self, user_id, display_name, phone):
        return db.update_profile(user_id, display_name, phone)
    def list_limited_patients(self):
        return db.list_limited_patients()
