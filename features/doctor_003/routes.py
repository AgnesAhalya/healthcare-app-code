from flask import Blueprint
from shared.extensions import csrf
from services.access_control import require_role
from services.feature_registry import run_feature

doctor_003_bp = Blueprint('doctor_003', __name__)


@doctor_003_bp.route('/doctor/notes/c2f', methods=['GET', 'POST'])
@csrf.exempt
@require_role('doctor_nurse')
def feature_page():
    return run_feature('doctor_003')
