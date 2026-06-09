from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

role_manager_005_bp = Blueprint('role_manager_005', __name__)


@role_manager_005_bp.route('/role-manager/session', methods=['GET', 'POST'])
@require_role('role_manager')
def feature_page():
    return run_feature('role_manager_005')
