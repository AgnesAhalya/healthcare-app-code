from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_maintainer_001_action

maintainer_001_bp = Blueprint('maintainer_001', __name__)


@maintainer_001_bp.route('/maintainer/backup', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    action = get_maintainer_001_action()

    return run_feature('maintainer_001', action)
