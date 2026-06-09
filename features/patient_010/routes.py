from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_010_action

patient_010_bp = Blueprint('patient_010', __name__)


@patient_010_bp.route('/outpatient/records/download', methods=['GET', 'POST'])
@patient_010_bp.route('/outpatient/records/path', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    action = get_patient_010_action()

    return run_feature('patient_010', action)
