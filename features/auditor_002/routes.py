from flask import Blueprint, abort, g, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_auditor_002_action
auditor_002_bp = Blueprint('auditor_002', __name__)


@auditor_002_bp.route('/auditor-api-keys-store', methods=['GET', 'POST'])
@require_role('security_auditor')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_auditor_002_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("auditor_002", message=message, result=result, actor=actor)
