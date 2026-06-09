from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_doctor_001_action

doctor_001_bp = Blueprint('doctor_001', __name__)


@doctor_001_bp.route('/doctor/appointments', methods=['GET', 'POST'])
@require_role('doctor_nurse')
def feature_page():
    action = get_doctor_001_action()

    return run_feature('doctor_001', action)
