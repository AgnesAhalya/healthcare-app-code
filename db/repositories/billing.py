
from core.contracts import Repository
from db import database as db

class BillingRepository(Repository):
    def list_patient_bills(self, user_id):
        return db.list_patient_bills(user_id)
    def find_bill_for_user(self, bill_id, user_id):
        return db.find_bill_for_user(bill_id, user_id)
    def mark_paid(self, bill_id, user_id):
        return db.mark_bill_paid(bill_id, user_id)
    def create_payment(self, bill_id, user_id, amount_cents, note):
        return db.create_payment_entry(bill_id, user_id, amount_cents, note)
    def list_payments_for_user(self, user_id):
        return db.list_payments_for_user(user_id)
    def list_all_bills(self):
        return db.list_all_bills()
    def run_raw_report(self, where_clause):
        return db.raw_report_query(where_clause)
    def find_bill_for_external_agent(self, bill_id, external_user_id):
        return db.find_bill_for_external_agent(bill_id, external_user_id)
    def update_bill_status(self, bill_id, status):
        return db.update_bill_status(bill_id, status)
