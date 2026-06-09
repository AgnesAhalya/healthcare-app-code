from flask import Blueprint, g, render_template, request, session, redirect, url_for

from auth.session_service import require_inpatient_ui_auth, require_outpatient_ui_auth
from db.database import find_profile_by_user_id, update_profile
import re

patient_007_bp = Blueprint("patient_007", __name__)


def render_patient_profile_page(expected_usertype):
    current_session = getattr(g, "current_session", None)

    if current_session is None:
        session.clear()
        return redirect(url_for("patient_002.login_page"))

    if current_session.user_type != expected_usertype:
        session.clear()
        return redirect(url_for("patient_002.login_page"))

    message = None
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        phone = request.form.get("phone", "").strip()
        PHONE_RE = re.compile(r"^\+?[0-9][0-9\s().-]{6,19}$")

        if not display_name:
            message = "Display name is required"
        elif not phone:
            message = "Phone number is required"
        elif not PHONE_RE.fullmatch(phone):
            message = "Enter a valid phone number"
        else:
            update_profile(current_session.user_id, display_name, phone)
            message = "Profile updated"

    profile = find_profile_by_user_id(current_session.user_id)

    if profile is None:
        return "Profile not found", 404

    return render_template(
        "patient_profile.html",
        profile=profile,
        usertype=expected_usertype,
        message=message,
    )


@patient_007_bp.route("/inpatient/profile", methods=["GET", "POST"])
@require_inpatient_ui_auth
def inpatient_profile_page():
    return render_patient_profile_page("inpatient")


@patient_007_bp.route("/outpatient/profile", methods=["GET", "POST"])
@require_outpatient_ui_auth
def outpatient_profile_page():
    return render_patient_profile_page("outpatient")
