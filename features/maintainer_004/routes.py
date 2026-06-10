from flask import Blueprint, abort, g, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_maintainer_004_action

maintainer_004_bp = Blueprint('maintainer_004', __name__)


@maintainer_004_bp.route('/maintainer/banner', methods=['GET', 'POST'])
@require_role('maintainer')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_maintainer_004_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("maintainer_004", message=message, result=result, actor=actor)
