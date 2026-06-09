from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_003_action

patient_003_bp = Blueprint('patient_003', __name__)


@patient_003_bp.route('/outpatient/payment-amount', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_003_action()

    return run_feature('patient_003', action)
