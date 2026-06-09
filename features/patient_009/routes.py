from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

patient_009_bp = Blueprint('patient_009', __name__)


@patient_009_bp.route('/outpatient/records/dsce', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    return run_feature('patient_009')
