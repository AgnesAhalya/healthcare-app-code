from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_maintainer_003_action

maintainer_003_bp = Blueprint('maintainer_003', __name__)


@maintainer_003_bp.route('/maintainer/banner-e2g', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    action = get_maintainer_003_action()

    return run_feature('maintainer_003', action)
