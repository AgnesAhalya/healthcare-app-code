from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_auditor_003_action
auditor_003_bp = Blueprint('auditor_003', __name__)


@auditor_003_bp.route('/auditor-audit', methods=['GET', 'POST'])
@require_role('security_auditor')
def feature_page():
    action = get_auditor_003_action("default")
    return run_feature('auditor_003')
