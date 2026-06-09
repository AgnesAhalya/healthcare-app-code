from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

auditor_004_bp = Blueprint('auditor_004', __name__)


@auditor_004_bp.route('/auditor-logs-write', methods=['GET', 'POST'])
@require_role('security_auditor')
def feature_page():
    return run_feature('auditor_004')
