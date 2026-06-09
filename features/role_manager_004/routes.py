from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_role_manager_004_action

role_manager_004_bp = Blueprint('role_manager_004', __name__)


@role_manager_004_bp.route('/role-manager/export', methods=['GET', 'POST'])
@require_role('role_manager')
def feature_page():
    action = get_role_manager_004_action()

    return run_feature('role_manager_004', action)
