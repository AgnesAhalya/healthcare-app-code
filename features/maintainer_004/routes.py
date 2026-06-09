from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

maintainer_004_bp = Blueprint('maintainer_004', __name__)


@ maintainer_004_bp.route('/maintainer/banner', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    return run_feature('maintainer_004')
