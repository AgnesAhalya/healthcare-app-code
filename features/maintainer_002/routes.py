from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

maintainer_002_bp = Blueprint('maintainer_002', __name__)


@ maintainer_002_bp.route('/maintainer/backup-mass', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    return run_feature('maintainer_002')
