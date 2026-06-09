from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

external_001_bp = Blueprint('external_001', __name__)


@external_001_bp.route('/external/records/parse', methods=['GET', 'POST'])
@external_001_bp.route('/external/records', methods=['GET', 'POST'])
@require_role('external_user')
def feature_page():
    return run_feature('external_001')
