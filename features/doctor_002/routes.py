from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

doctor_002_bp = Blueprint('doctor_002', __name__)


@doctor_002_bp.route('/doctor/employee-record', methods=['GET', 'POST'])
@require_role('doctor_nurse')
def feature_page():
    return run_feature('doctor_002')
