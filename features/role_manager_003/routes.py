from flask import Blueprint, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_role_manager_003_action

role_manager_003_bp = Blueprint('role_manager_003', __name__)


@role_manager_003_bp.route('/role-manager/config/path', methods=['GET', 'POST'])
@role_manager_003_bp.route('/role-manager/config', methods=['GET', 'POST'])
@require_role('role_manager')
def feature_page():
    action_name = request.form.get('action') or 'default'
    action = get_role_manager_003_action(action_name)

    return run_feature('role_manager_003', action)
