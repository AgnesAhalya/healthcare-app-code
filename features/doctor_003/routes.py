from flask import Blueprint
from shared.extensions import csrf
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_doctor_003_action

doctor_003_bp = Blueprint('doctor_003', __name__)


@doctor_003_bp.route('/doctor/notes/c2f', methods=['GET', 'POST'])
@csrf.exempt
@require_role('doctor_nurse')
def feature_page():
    action = get_doctor_003_action()

    return run_feature('doctor_003', action)