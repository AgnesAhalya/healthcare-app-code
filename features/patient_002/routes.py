from flask import Blueprint, request, render_template, redirect, session, url_for

import jwt
import uuid

from auth.session_service import authenticate, create_token, load_current_session
from db.database import revoke_session
from shared.rate_limiter import limiter


patient_002_bp = Blueprint("patient_002", __name__)

VALID_USER_TYPES = {
    "inpatient",
    "outpatient",
    "role_manager",
    "billing_staff",
    "doctor_nurse",
    "maintainer",
    "security_auditor",
    "external_user",
}

ROLE_HOME = {
    "inpatient": "patient_007.inpatient_profile_page",
    "outpatient": "patient_007.outpatient_profile_page",
    "role_manager": "role_manager_001.feature_page",
    "billing_staff": "billing_003.feature_page",
    "doctor_nurse": "doctor_002.feature_page",
    "maintainer": "maintainer_006.feature_page",
    "security_auditor": "auditor_003.feature_page",
    "external_user": "external_001.feature_page",
}


def username_rate_limit_key():
    body = request.get_json(silent=True)
    if body is None:
        username = request.form.get("username", "")
    else:
        username = body.get("username", "")
    username = username.strip().lower()
    if username:
        return f"login-user:{username}"
    if "empty_username_rl_id" not in session:
        session["empty_username_rl_id"] = uuid.uuid4().hex
    return f"login-empty-user:{session['empty_username_rl_id']}"


def revoke_token_session(token, usertype):
    try:
        current_session = load_current_session(token, usertype)
    except jwt.PyJWTError:
        return False
    if current_session is None:
        return False
    revoke_session(current_session.session_id)
    return True


def revoke_existing_ui_session():
    old_token = session.get("access_token")
    old_usertype = session.get("usertype")
    if old_token is None or old_usertype not in VALID_USER_TYPES:
        return
    try:
        current_session = load_current_session(old_token, old_usertype)
    except jwt.PyJWTError:
        return
    if current_session is not None:
        revoke_session(current_session.session_id)


@patient_002_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("30 per minute")
@limiter.limit("10 per minute", key_func=username_rate_limit_key)
def login_page():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        usertype = request.form.get("usertype", "")
        if usertype not in VALID_USER_TYPES:
            error = "Invalid user type"
            return render_template("patient_login.html", error=error)
        user = authenticate(username, password, usertype)
        if user is None:
            error = "Invalid username or password"
        else:
            revoke_existing_ui_session()
            token = create_token(user)
            session.clear()
            session["access_token"] = token
            session["usertype"] = usertype
            return redirect(url_for(ROLE_HOME[usertype]))
    return render_template("patient_login.html", error=error)


@patient_002_bp.route("/logout", methods=["POST"])
def logout_ui():
    token = session.get("access_token")
    usertype = session.get("usertype")
    if token is not None and usertype in VALID_USER_TYPES:
        revoke_token_session(token, usertype)
    session.clear()
    return redirect(url_for("patient_002.login_page"))
