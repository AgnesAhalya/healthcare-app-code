from functools import wraps
from flask import g, redirect, session, url_for
from auth.session_service import load_current_session
import jwt

ROLE_LABELS = {
    "inpatient": "Patient",
    "outpatient": "Patient",
    "role_manager": "Role Manager",
    "billing_staff": "Billing Staff",
    "doctor_nurse": "Doctor/Nurse",
    "maintainer": "Maintainer",
    "security_auditor": "Security Auditor",
    "external_user": "External User",
}

def require_role(expected_user_type):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            token = session.get("access_token")
            usertype = session.get("usertype")
            if token is None or usertype != expected_user_type:
                return redirect(url_for("patient_002.login_page"))
            try:
                current_session = load_current_session(token, expected_user_type)
            except jwt.PyJWTError:
                session.clear()
                return redirect(url_for("patient_002.login_page"))
            if current_session is None:
                session.clear()
                return redirect(url_for("patient_002.login_page"))
            g.current_session = current_session
            return view_func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_role(view_func):
    from functools import wraps
    from flask import g, redirect, session, url_for
    from auth.session_service import load_current_session

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        token = session.get("access_token")
        usertype = session.get("usertype")
        if token is None or usertype is None:
            return redirect(url_for("patient_002.login_page"))
        current_session = load_current_session(token, usertype)
        if current_session is None:
            session.clear()
            return redirect(url_for("patient_002.login_page"))
        g.current_session = current_session
        return view_func(*args, **kwargs)
    return wrapper
