from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_009_action

patient_009_bp = Blueprint('patient_009', __name__)


@patient_009_bp.route('/outpatient/records/dsce', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_009_action()

    return run_feature('patient_009', action)
