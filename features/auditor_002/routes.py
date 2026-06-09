from flask import Blueprint,request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_auditor_002_action
auditor_002_bp = Blueprint('auditor_002', __name__)


@auditor_002_bp.route('/auditor-api-keys-store', methods=['GET', 'POST'])
@require_role('security_auditor')
def feature_page():
    action = get_auditor_002_action("default")
    return run_feature('auditor_002',action=action)
