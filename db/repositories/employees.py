
from core.contracts import Repository
from db import database as db

class EmployeeRepository(Repository):
    def find_record(self, user_id):
        return db.find_employee_record(user_id)
    def update_record(self, user_id, emergency_contact, notes):
        return db.update_employee_record(user_id, emergency_contact, notes)
    def create_note(self, patient_user_id, author_user_id, note_body):
        return db.create_note(patient_user_id, author_user_id, note_body)
    def list_notes(self):
        return db.list_notes()
