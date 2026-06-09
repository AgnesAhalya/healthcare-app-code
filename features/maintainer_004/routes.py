from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_maintainer_004_action

maintainer_004_bp = Blueprint('maintainer_004', __name__)


@maintainer_004_bp.route('/maintainer/banner', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    action = get_maintainer_004_action()

    return run_feature('maintainer_004', action)
