from flask import Blueprint, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_maintainer_002_action

maintainer_002_bp = Blueprint('maintainer_002', __name__)


@maintainer_002_bp.route('/maintainer/backup-mass', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    action_name = request.form.get('action') or 'default'
    action = get_maintainer_002_action(action_name)

    return run_feature('maintainer_002', action)
