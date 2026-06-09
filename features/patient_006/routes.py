from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_006_action

patient_006_bp = Blueprint('patient_006', __name__)


@patient_006_bp.route('/outpatient/bills', methods=['GET', 'POST'])
@patient_006_bp.route('/outpatient/payments', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_006_action()

    return run_feature('patient_006', action)
