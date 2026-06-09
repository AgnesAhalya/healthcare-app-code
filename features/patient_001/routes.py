from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_001_action

patient_001_bp = Blueprint('patient_001', __name__)


@patient_001_bp.route('/outpatient/appointments/schedule', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_001_action()

    return run_feature('patient_001', action)
