from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_doctor_004_action

doctor_004_bp = Blueprint('doctor_004', __name__)


@doctor_004_bp.route('/doctor/notes', methods=['GET', 'POST'])
@require_role('doctor_nurse')
def feature_page():
    action = get_doctor_004_action()

    return run_feature('doctor_004', action)
