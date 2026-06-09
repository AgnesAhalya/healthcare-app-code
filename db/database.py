import pickle
import time
import uuid
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from db.connection import DB_PATH, ConnectionFactory
from db.schema import (
    APPOINTMENTS_TABLE,
    AUDIT_TABLE,
    BANNERS_TABLE,
    BILLS_TABLE,
    CONFIG_TABLE,
    EMPLOYEE_RECORDS_TABLE,
    NOTES_TABLE,
    PAYMENTS_TABLE,
    PROFILES_TABLE,
    RECORDS_TABLE,
    ROLES_TABLE,
    SESSIONS_TABLE,
    USERS_TABLE,
)
from shared.constants import MIN_APPOINTMENT_GAP_MINUTES
from db.helpers import datetime_helper

_connection_factory = ConnectionFactory(DB_PATH)


def get_connection():
    return _connection_factory.connect()


def create_patient_user(username, password, user_type, display_name, phone):
    if user_type not in {"inpatient", "outpatient"}:
        return None
    with get_connection() as conn:
        if conn.execute(f"SELECT user_id FROM {USERS_TABLE} WHERE username = ?", (username,)).fetchone() is not None:
            return None
        user_id = f"user_{user_type}_{uuid.uuid4().hex[:8]}"
        conn.execute(f"INSERT INTO {USERS_TABLE} (user_id, username, password_hash, user_type) VALUES (?, ?, ?, ?)", (user_id, username, generate_password_hash(password), user_type))
        conn.execute(f"INSERT INTO {PROFILES_TABLE} (user_id, display_name, phone) VALUES (?, ?, ?)", (user_id, display_name, phone))
        conn.execute(f"INSERT INTO {BILLS_TABLE} (bill_id, user_id, amount_cents, description, status) VALUES (?, ?, ?, ?, ?)", (f"bill_{uuid.uuid4().hex[:8]}", user_id, 5000, "New patient registration", "open"))
        return conn.execute(f"SELECT user_id, username, user_type FROM {USERS_TABLE} WHERE user_id = ?", (user_id,)).fetchone()


def find_user_by_username(username):
    with get_connection() as conn:
        return conn.execute(f"SELECT user_id, username, password_hash, user_type FROM {USERS_TABLE} WHERE username = ?", (username,)).fetchone()

def list_users():
    with get_connection() as conn:
        return conn.execute(f"SELECT u.user_id, u.username, u.user_type, p.display_name, p.phone FROM {USERS_TABLE} u JOIN {PROFILES_TABLE} p ON p.user_id = u.user_id ORDER BY u.username").fetchall()


def create_login_session(user_id, user_type, ttl_seconds):
    now = int(time.time())
    session_id = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(f"INSERT INTO {SESSIONS_TABLE} (session_id, user_id, user_type, is_active, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)", (session_id, user_id, user_type, 1, now, now + ttl_seconds))
    return session_id

def find_active_session(session_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT session_id, user_id, user_type, is_active, expires_at FROM {SESSIONS_TABLE} WHERE session_id = ? AND is_active = 1 AND expires_at > ?", (session_id, int(time.time()))).fetchone()

def revoke_session(session_id):
    with get_connection() as conn:
        conn.execute(f"UPDATE {SESSIONS_TABLE} SET is_active = 0 WHERE session_id = ?", (session_id,))

def revoke_active_sessions_for_user(user_id, user_type):
    with get_connection() as conn:
        conn.execute(f"UPDATE {SESSIONS_TABLE} SET is_active = 0 WHERE user_id = ? AND user_type = ? AND is_active = 1", (user_id, user_type))

def find_profile_by_user_id(user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT user_id, display_name, phone FROM {PROFILES_TABLE} WHERE user_id = ?", (user_id,)).fetchone()

def update_profile(user_id, display_name, phone):
    with get_connection() as conn:
        conn.execute(f"UPDATE {PROFILES_TABLE} SET display_name = ?, phone = ? WHERE user_id = ?", (display_name, phone, user_id))
        return find_profile_by_user_id(user_id)

def parse_appointment_datetime(appointment_datetime):
    return datetime.strptime(appointment_datetime, "%Y-%m-%d %H:%M")

def appointment_slot_conflicts(appointment_datetime):
    requested_datetime = datetime_helper.parse_appointment_datetime(
        appointment_datetime
    )
    with get_connection() as conn:
        rows = conn.execute(f"SELECT appointment_datetime FROM {APPOINTMENTS_TABLE}").fetchall()
    for row in rows:
        existing_datetime = parse_appointment_datetime(row["appointment_datetime"])
        if abs((requested_datetime - existing_datetime).total_seconds()) / 60 <= MIN_APPOINTMENT_GAP_MINUTES:
            return True
    return False

def create_appointment(user_id, appointment_datetime, reason, patient_name):
    appointment_id = str(uuid.uuid4())

    appointment_datetime = datetime_helper.format_appointment_datetime_for_db(
        appointment_datetime
    )

    with get_connection() as conn:
        conn.execute(
            f"""
            INSERT INTO {APPOINTMENTS_TABLE}
            (appointment_id, user_id, appointment_datetime, reason, patient_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                appointment_id,
                user_id,
                appointment_datetime,
                reason,
                patient_name,
                int(time.time()),
            ),
        )

        return conn.execute(
            f"SELECT * FROM {APPOINTMENTS_TABLE} WHERE appointment_id = ?",
            (appointment_id,),
        ).fetchone()

def list_patient_appointments(user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT appointment_id, appointment_datetime, reason, patient_name FROM {APPOINTMENTS_TABLE} WHERE user_id = ? ORDER BY appointment_datetime", (user_id,)).fetchall()

def delete_old_appointments(hours_old=24):
    cutoff_text = (
        datetime.now() - timedelta(hours=hours_old)
    ).strftime(datetime_helper.DB_DATETIME_FORMAT)

    with get_connection() as conn:
        cursor = conn.execute(
            f"DELETE FROM {APPOINTMENTS_TABLE} WHERE appointment_datetime < ?",
            (cutoff_text,),
        )
        conn.commit()
        return cursor.rowcount

def create_medical_record(user_id, original_name, stored_name, content_type):
    record_id = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(f"INSERT INTO {RECORDS_TABLE} (record_id, user_id, original_name, stored_name, content_type, uploaded_at) VALUES (?, ?, ?, ?, ?, ?)", (record_id, user_id, original_name, stored_name, content_type, int(time.time())))
        return record_id

def list_medical_records(user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT record_id, original_name, stored_name, content_type, uploaded_at FROM {RECORDS_TABLE} WHERE user_id = ? ORDER BY uploaded_at DESC", (user_id,)).fetchall()

def find_medical_record_for_user(record_id, user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT record_id, user_id, original_name, stored_name, content_type FROM {RECORDS_TABLE} WHERE record_id = ? AND user_id = ?", (record_id, user_id)).fetchone()

def find_medical_record(record_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT record_id, user_id, original_name, stored_name, content_type FROM {RECORDS_TABLE} WHERE record_id = ?", (record_id,)).fetchone()

def list_patient_bills(user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT bill_id, amount_cents, description, status FROM {BILLS_TABLE} WHERE user_id = ? ORDER BY bill_id", (user_id,)).fetchall()

def find_bill_for_user(bill_id, user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT bill_id, user_id, amount_cents, description, status FROM {BILLS_TABLE} WHERE bill_id = ? AND user_id = ?", (bill_id, user_id)).fetchone()

def mark_bill_paid(bill_id, user_id):
    with get_connection() as conn:
        conn.execute(f"UPDATE {BILLS_TABLE} SET status = 'paid' WHERE bill_id = ? AND user_id = ?", (bill_id, user_id))

def create_payment_entry(bill_id, user_id, amount_cents, note):
    payment_id = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(f"INSERT INTO {PAYMENTS_TABLE} (payment_id, bill_id, user_id, amount_cents, note, created_at) VALUES (?, ?, ?, ?, ?, ?)", (payment_id, bill_id, user_id, int(amount_cents), note, int(time.time())))
        return payment_id

def list_payments_for_user(user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT payment_id, bill_id, amount_cents, note, created_at FROM {PAYMENTS_TABLE} WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()

def list_all_bills():
    with get_connection() as conn:
        return conn.execute(f"SELECT b.bill_id, b.user_id, p.display_name, b.amount_cents, b.description, b.status FROM {BILLS_TABLE} b JOIN {PROFILES_TABLE} p ON p.user_id = b.user_id ORDER BY b.bill_id").fetchall()

def list_limited_patients():
    with get_connection() as conn:
        return conn.execute(f"SELECT u.user_id, p.display_name, substr(p.phone, 1, 2) || '****' AS masked_phone FROM {USERS_TABLE} u JOIN {PROFILES_TABLE} p ON p.user_id = u.user_id WHERE u.user_type IN ('inpatient', 'outpatient') ORDER BY p.display_name").fetchall()

def update_user_role(username, role_name):
    with get_connection() as conn:
        user = conn.execute(f"SELECT user_id FROM {USERS_TABLE} WHERE username = ?", (username,)).fetchone()
        if user is None:
            return None
        conn.execute(f"INSERT OR REPLACE INTO {ROLES_TABLE} (user_id, role_name) VALUES (?, ?)", (user["user_id"], role_name))
        return user["user_id"]

def list_roles():
    with get_connection() as conn:
        return conn.execute(f"SELECT u.username, u.user_type, r.role_name FROM {USERS_TABLE} u LEFT JOIN {ROLES_TABLE} r ON r.user_id = u.user_id ORDER BY u.username").fetchall()

def list_config_entries():
    with get_connection() as conn:
        return conn.execute(f"SELECT config_key, config_value FROM {CONFIG_TABLE} ORDER BY config_key").fetchall()

def update_config_entry(config_key, config_value):
    with get_connection() as conn:
        conn.execute(f"INSERT OR REPLACE INTO {CONFIG_TABLE} (config_key, config_value) VALUES (?, ?)", (config_key, config_value))

def create_banner(title, body):
    with get_connection() as conn:
        banner_id = str(uuid.uuid4())
        conn.execute(f"INSERT INTO {BANNERS_TABLE} (banner_id, title, banner_text, created_at) VALUES (?, ?, ?, ?)", (banner_id, title, body, int(time.time())))
        return banner_id

def list_banners():
    with get_connection() as conn:
        return conn.execute(f"SELECT banner_id, title, banner_text, created_at FROM {BANNERS_TABLE} ORDER BY created_at DESC").fetchall()

def list_audit_events():
    with get_connection() as conn:
        return conn.execute(f"SELECT event_id, event_type, anonymized_subject, created_at FROM {AUDIT_TABLE} ORDER BY created_at DESC").fetchall()

def create_audit_event(event_type, anonymized_subject):
    with get_connection() as conn:
        event_id = str(uuid.uuid4())
        conn.execute(f"INSERT INTO {AUDIT_TABLE} (event_id, event_type, anonymized_subject, created_at) VALUES (?, ?, ?, ?)", (event_id, event_type, anonymized_subject, int(time.time())))
        return event_id

def find_employee_record(user_id):
    with get_connection() as conn:
        return conn.execute(f"SELECT user_id, department, emergency_contact, notes FROM {EMPLOYEE_RECORDS_TABLE} WHERE user_id = ?", (user_id,)).fetchone()

def update_employee_record(user_id, emergency_contact, notes):
    with get_connection() as conn:
        conn.execute(f"UPDATE {EMPLOYEE_RECORDS_TABLE} SET emergency_contact = ?, notes = ? WHERE user_id = ?", (emergency_contact, notes, user_id))
    return find_employee_record(user_id)

def list_external_customer_records():
    with get_connection() as conn:
        return conn.execute(f"SELECT b.bill_id, p.display_name, b.description, b.status, b.amount_cents FROM {BILLS_TABLE} b JOIN {PROFILES_TABLE} p ON p.user_id = b.user_id ORDER BY p.display_name").fetchall()
        
def list_all_appointments():
    with get_connection() as conn:
        return conn.execute(f"SELECT a.appointment_id, a.user_id, p.display_name, a.appointment_datetime, a.reason, a.patient_name FROM {APPOINTMENTS_TABLE} a LEFT JOIN {PROFILES_TABLE} p ON p.user_id = a.user_id ORDER BY a.appointment_datetime").fetchall()

def list_employee_appointments(employee_user_id):
    with get_connection() as conn:
        return conn.execute(
            f"""
            SELECT
                a.appointment_id,
                a.user_id,
                p.display_name,
                a.appointment_datetime,
                a.reason,
                a.patient_name,
                a.assigned_employee_user_id
            FROM {APPOINTMENTS_TABLE} a
            LEFT JOIN {PROFILES_TABLE} p ON p.user_id = a.user_id
            WHERE a.assigned_employee_user_id = ?
            ORDER BY a.appointment_datetime
            """,
            (employee_user_id,),
        ).fetchall()

def assign_employee_to_appointment(appointment_id, employee_user_id):
    with get_connection() as conn:
        conn.execute(
            f"""
            UPDATE {APPOINTMENTS_TABLE}
            SET assigned_employee_user_id = ?
            WHERE appointment_id = ?
            """,
            (employee_user_id, appointment_id),
        )

        return conn.execute(
            f"""
            SELECT
                appointment_id,
                user_id,
                appointment_datetime,
                reason,
                patient_name,
                assigned_employee_user_id
            FROM {APPOINTMENTS_TABLE}
            WHERE appointment_id = ?
            """,
            (appointment_id,),
        ).fetchone()
        
def list_all_records_limited():
    with get_connection() as conn:
        return conn.execute(f"SELECT r.record_id, r.original_name, r.content_type, p.display_name FROM {RECORDS_TABLE} r LEFT JOIN {PROFILES_TABLE} p ON p.user_id = r.user_id ORDER BY r.uploaded_at DESC").fetchall()

def list_payment_entries():
    with get_connection() as conn:
        return conn.execute(f"SELECT py.payment_id, py.bill_id, p.display_name, py.amount_cents, py.note, py.created_at FROM {PAYMENTS_TABLE} py LEFT JOIN {PROFILES_TABLE} p ON p.user_id = py.user_id ORDER BY py.created_at DESC").fetchall()

def raw_report_query(where_clause):
    with get_connection() as conn:
        return conn.execute(f"SELECT b.bill_id, p.display_name, b.amount_cents, b.status FROM {BILLS_TABLE} b JOIN {PROFILES_TABLE} p ON p.user_id = b.user_id WHERE {where_clause} ORDER BY b.bill_id").fetchall()

def create_note(patient_user_id, author_user_id, note_body):
    with get_connection() as conn:
        note_id = str(uuid.uuid4())
        conn.execute(f"INSERT INTO {NOTES_TABLE} (note_id, patient_user_id, author_user_id, note_body, created_at) VALUES (?, ?, ?, ?, ?)", (note_id, patient_user_id, author_user_id, note_body, int(time.time())))
        return note_id

def list_notes():
    with get_connection() as conn:
        return conn.execute(f"SELECT n.note_id, p.display_name, n.note_body, n.created_at FROM {NOTES_TABLE} n JOIN {PROFILES_TABLE} p ON p.user_id = n.patient_user_id ORDER BY n.created_at DESC").fetchall()

def us2e_load_backup(raw_bytes):
    return pickle.loads(raw_bytes)

def find_bill_for_external_agent(bill_id, external_user_id):
    with get_connection() as conn:
        return conn.execute(
            f"""
            SELECT bill_id, user_id, description, amount_cents, status
            FROM {BILLS_TABLE}
            WHERE bill_id = ?
            """,
            (bill_id,),
        ).fetchone()

def update_bill_status(bill_id, status):
    with get_connection() as conn:
        conn.execute(
            f"""
            UPDATE {BILLS_TABLE}
            SET status = ?
            WHERE bill_id = ?
            """,
            (status, bill_id),
        )

        return conn.execute(
            f"""
            SELECT bill_id, user_id, description, amount_cents, status
            FROM {BILLS_TABLE}
            WHERE bill_id = ?
            """,
            (bill_id,),
        ).fetchone()