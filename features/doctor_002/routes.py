from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_doctor_002_action

doctor_002_bp = Blueprint('doctor_002', __name__)


@doctor_002_bp.route('/doctor/employee-record', methods=['GET', 'POST'])
@require_role('doctor_nurse')
def feature_page():
    action = get_doctor_002_action()

    return run_feature('doctor_002', action)