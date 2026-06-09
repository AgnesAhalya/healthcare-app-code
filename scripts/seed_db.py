"""Seed deterministic healthcare test data for the healthcare MVP."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


import os
import time

from werkzeug.security import generate_password_hash

from db.connection import ConnectionFactory
from db.schema import (
    AUDIT_TABLE,
    BANNERS_TABLE,
    BILLS_TABLE,
    CONFIG_TABLE,
    EMPLOYEE_RECORDS_TABLE,
    PROFILES_TABLE,
    ROLES_TABLE,
    USERS_TABLE,
)
from shared.constants import MIN_APPOINTMENT_GAP_MINUTES


def password_for(env_name: str, fallback: str) -> str:
    return os.environ.get(env_name, fallback)


def seed_user(conn, user_id: str, username: str, password: str, user_type: str, display_name: str, phone: str) -> None:
    conn.execute(
        f"""
        INSERT OR IGNORE INTO {USERS_TABLE}
            (user_id, username, password_hash, user_type)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, username, generate_password_hash(password), user_type),
    )
    conn.execute(
        f"""
        INSERT OR IGNORE INTO {PROFILES_TABLE}
            (user_id, display_name, phone)
        VALUES (?, ?, ?)
        """,
        (user_id, display_name, phone),
    )


def seed_users(conn) -> None:
    seed_user(conn, "user_inpatient_1", "inpatient", password_for("INPATIENT_PASSWORD", "inpatient-pass"), "inpatient", "Inpatient User", "111111")
    seed_user(conn, "user_outpatient_1", "outpatient", password_for("OUTPATIENT_PASSWORD", "outpatient-pass"), "outpatient", "Outpatient User", "222222")
    seed_user(conn, "user_rolemanager_1", "rolemanager", password_for("STAFF_PASSWORD", "staff-pass"), "role_manager", "Role Manager", "333333")
    seed_user(conn, "user_billing_1", "billing", password_for("STAFF_PASSWORD", "staff-pass"), "billing_staff", "Billing Staff", "444444")
    seed_user(conn, "user_doctor_1", "doctor", password_for("STAFF_PASSWORD", "staff-pass"), "doctor_nurse", "Doctor User", "555555")
    seed_user(conn, "user_maintainer_1", "maintainer", password_for("STAFF_PASSWORD", "staff-pass"), "maintainer", "Maintainer User", "666666")
    seed_user(conn, "user_auditor_1", "auditor", password_for("STAFF_PASSWORD", "staff-pass"), "security_auditor", "Security Auditor", "777777")
    seed_user(conn, "user_external_1", "external", password_for("EXTERNAL_PASSWORD", "external-pass"), "external_user", "External Partner", "888888")


def seed_employee_roles(conn) -> None:
    employees = [
        ("user_rolemanager_1", "role_manager"),
        ("user_billing_1", "billing_staff"),
        ("user_doctor_1", "doctor_nurse"),
        ("user_maintainer_1", "maintainer"),
        ("user_auditor_1", "security_auditor"),
    ]
    for user_id, role_name in employees:
        conn.execute(
            f"INSERT OR IGNORE INTO {ROLES_TABLE} (user_id, role_name) VALUES (?, ?)",
            (user_id, role_name),
        )
        conn.execute(
            f"""
            INSERT OR IGNORE INTO {EMPLOYEE_RECORDS_TABLE}
                (user_id, department, emergency_contact, notes)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, role_name.replace("_", " ").title(), "999999", "Own employee record"),
        )


def seed_business_data(conn) -> None:
    now = int(time.time())
    conn.execute(f"INSERT OR IGNORE INTO {CONFIG_TABLE} (config_key, config_value) VALUES (?, ?)", ("site_name", "Healthcare Portal"))
    conn.execute(f"INSERT OR IGNORE INTO {CONFIG_TABLE} (config_key, config_value) VALUES (?, ?)", ("appointment_gap", str(MIN_APPOINTMENT_GAP_MINUTES)))
    conn.execute(f"INSERT OR IGNORE INTO {BILLS_TABLE} (bill_id, user_id, amount_cents, description, status) VALUES (?, ?, ?, ?, ?)", ("bill_outpatient_1", "user_outpatient_1", 7500, "General consultation", "open"))
    conn.execute(f"INSERT OR IGNORE INTO {BILLS_TABLE} (bill_id, user_id, amount_cents, description, status) VALUES (?, ?, ?, ?, ?)", ("bill_inpatient_1", "user_inpatient_1", 13000, "Inpatient service", "open"))
    conn.execute(f"INSERT OR IGNORE INTO {AUDIT_TABLE} (event_id, event_type, anonymized_subject, created_at) VALUES (?, ?, ?, ?)", ("audit_1", "profile_view", "patient-8e3f", now))
    conn.execute(f"INSERT OR IGNORE INTO {BANNERS_TABLE} (banner_id, title, banner_text, created_at) VALUES (?, ?, ?, ?)", ("banner_1", "Checkup Reminder", "Annual checkups are available this month.", now))


def main():
    with ConnectionFactory().connect() as conn:
        seed_users(conn)
        seed_employee_roles(conn)
        seed_business_data(conn)
    print("[db-seed] healthcare test data ready")


if __name__ == "__main__":
    main()
