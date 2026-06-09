from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_auditor_005_action

auditor_005_bp = Blueprint('auditor_005', __name__)


@auditor_005_bp.route('/auditor/logs', methods=['GET', 'POST'])
@require_role('security_auditor')
def feature_page():
    action = get_auditor_005_action()

    return run_feature('auditor_005', action)
