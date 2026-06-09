from flask import Blueprint
from shared.extensions import csrf
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_004_action

patient_004_bp = Blueprint('patient_004', __name__)


@patient_004_bp.route('/maintainer/c2f', methods=['GET', 'POST'])
@csrf.exempt
@require_role('outpatient')
def feature_page():
    action = get_patient_004_action()

    return run_feature('patient_004', action)
