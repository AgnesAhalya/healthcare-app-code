from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from db.database import create_patient_user
from shared.rate_limiter import limiter


patient_013_bp = Blueprint("patient_013", __name__)

VALID_PATIENT_TYPES = {"inpatient", "outpatient"}


def signup_rate_limit_key():
    if request.is_json:
        body = request.get_json(silent=True) or {}
        username = body.get("username", "")
    else:
        username = request.form.get("username", "")

    username = username.strip().lower() or "missing-username"

    return f"signup-user:{username}"


@patient_013_bp.route("/signup", methods=["GET", "POST"])
@limiter.limit("6 per minute")
@limiter.limit("24 per day", key_func=signup_rate_limit_key)
def signup_page():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user_type = "outpatient"
        display_name = request.form.get("display_name", "").strip()
        phone = request.form.get("phone", "").strip()

        if user_type not in VALID_PATIENT_TYPES:
            error = "Invalid patient type"
        elif not username or not password or not display_name or not phone:
            error = "All fields are required"
        else:
            user = create_patient_user(
                username,
                password,
                user_type,
                display_name,
                phone
            )

            if user is None:
                error = "Username already exists"
            else:
                return redirect(url_for("patient_002.login_page"))

    return render_template("patient_signup.html", error=error)

