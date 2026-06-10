from flask import Blueprint, abort, g, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_external_001_action

external_001_bp = Blueprint('external_001', __name__)


@external_001_bp.route('/external/records/parse', methods=['GET', 'POST'])
@external_001_bp.route('/external/records', methods=['GET', 'POST'])
@require_role('external_user')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_external_001_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("external_001", message=message, result=result, actor=actor)
