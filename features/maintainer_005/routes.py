from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

maintainer_005_bp = Blueprint('maintainer_005', __name__)


@ maintainer_005_bp.route('/maintainer/c2l', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    return run_feature('maintainer_005')
