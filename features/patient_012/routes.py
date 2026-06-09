from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

patient_012_bp = Blueprint('patient_012', __name__)


@patient_012_bp.route('/outpatient/records', methods=['GET', 'POST'])
@patient_012_bp.route('/outpatient/records/upload', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    return run_feature('patient_012')
