
from core.contracts import Repository
from db import database as db

class AppointmentRepository(Repository):
    def has_conflict(self, appointment_datetime):
        return db.appointment_slot_conflicts(appointment_datetime)
    def create(self, user_id, appointment_datetime, reason, patient_name):
        return db.create_appointment(user_id, appointment_datetime, reason, patient_name)
    def list_for_patient(self, user_id):
        return db.list_patient_appointments(user_id)
    def list_all(self):
        return db.list_all_appointments()
    def delete_old(self, hours_old=24):
        return db.delete_old_appointments(hours_old)
    def list_for_employee(self, employee_user_id):
        return db.list_employee_appointments(employee_user_id)
    def assign_employee(self, appointment_id, employee_user_id):
        return db.assign_employee_to_appointment(appointment_id, employee_user_id)
