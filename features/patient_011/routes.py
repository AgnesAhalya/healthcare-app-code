from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_011_action

patient_011_bp = Blueprint('patient_011', __name__)


@patient_011_bp.route('/outpatient/records/s2e', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_011_action()

    return run_feature('patient_011', action)
