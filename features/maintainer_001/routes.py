from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

maintainer_001_bp = Blueprint('maintainer_001', __name__)



@maintainer_001_bp.route('/maintainer/backup', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    return run_feature('maintainer_001')
