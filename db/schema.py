"""Database table names and schema creation for the healthcare MVP."""

USERS_TABLE = "HEALTHCARE_001_users"
PROFILES_TABLE = "HEALTHCARE_001_profiles"
SESSIONS_TABLE = "HEALTHCARE_001_sessions"
APPOINTMENTS_TABLE = "HEALTHCARE_001_outpatient_appointments"
RECORDS_TABLE = "HEALTHCARE_001_medical_records"
BILLS_TABLE = "HEALTHCARE_001_bills"
PAYMENTS_TABLE = "HEALTHCARE_001_payments"
ROLES_TABLE = "HEALTHCARE_001_roles"
CONFIG_TABLE = "HEALTHCARE_001_config"
BANNERS_TABLE = "HEALTHCARE_001_banners"
AUDIT_TABLE = "HEALTHCARE_001_audit_events"
EMPLOYEE_RECORDS_TABLE = "HEALTHCARE_001_employee_records"
NOTES_TABLE = "HEALTHCARE_001_doctor_notes"


SCHEMA_STATEMENTS = (
    f"""
    CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
        user_id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        user_type TEXT NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {PROFILES_TABLE} (
        user_id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES {USERS_TABLE}(user_id)
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {SESSIONS_TABLE} (
        session_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        user_type TEXT NOT NULL,
        is_active INTEGER NOT NULL,
        created_at INTEGER NOT NULL,
        expires_at INTEGER NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {APPOINTMENTS_TABLE} (
        appointment_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        appointment_datetime TEXT NOT NULL,
        reason TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        assigned_employee_user_id TEXT DEFAULT NULL,
        created_at INTEGER NOT NULL,
        FOREIGN KEY(assigned_employee_user_id) REFERENCES {USERS_TABLE}(user_id)
        )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {RECORDS_TABLE} (
        record_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        original_name TEXT NOT NULL,
        stored_name TEXT NOT NULL,
        content_type TEXT NOT NULL,
        uploaded_at INTEGER NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {BILLS_TABLE} (
        bill_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {PAYMENTS_TABLE} (
        payment_id TEXT PRIMARY KEY,
        bill_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        note TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {ROLES_TABLE} (
        user_id TEXT PRIMARY KEY,
        role_name TEXT NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {CONFIG_TABLE} (
        config_key TEXT PRIMARY KEY,
        config_value TEXT NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {BANNERS_TABLE} (
        banner_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        banner_text TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {AUDIT_TABLE} (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        anonymized_subject TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {EMPLOYEE_RECORDS_TABLE} (
        user_id TEXT PRIMARY KEY,
        department TEXT NOT NULL,
        emergency_contact TEXT NOT NULL,
        notes TEXT NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {NOTES_TABLE} (
        note_id TEXT PRIMARY KEY,
        patient_user_id TEXT NOT NULL,
        author_user_id TEXT NOT NULL,
        note_body TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
    """,
)


def create_schema(conn):
    """Create every table required by the MVP application."""
    for statement in SCHEMA_STATEMENTS:
        conn.execute(statement)
