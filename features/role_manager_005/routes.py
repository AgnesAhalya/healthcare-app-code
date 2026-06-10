from flask import Blueprint, abort, g, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_role_manager_005_action

role_manager_005_bp = Blueprint('role_manager_005', __name__)


@role_manager_005_bp.route('/role-manager/session', methods=['GET', 'POST'])
@require_role('role_manager')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action_name = request.form.get("action") or "default"
        action = get_role_manager_005_action(action_name)
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("role_manager_005", message=message, result=result, actor=actor)
