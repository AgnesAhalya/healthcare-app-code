from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_maintainer_006_action

maintainer_006_bp = Blueprint('maintainer_006', __name__)


@maintainer_006_bp.route('/maintainer/awareness', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    action = get_maintainer_006_action()

    return run_feature('maintainer_006', action)