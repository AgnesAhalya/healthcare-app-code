from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_005_action

patient_005_bp = Blueprint('patient_005', __name__)


@patient_005_bp.route('/outpatient/payments/i2y', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_005_action()

    return run_feature('patient_005', action)
