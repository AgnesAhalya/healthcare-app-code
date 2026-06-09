from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

patient_005_bp = Blueprint('patient_005', __name__)



@patient_005_bp.route('/outpatient/payments/i2y', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    return run_feature('patient_005')
