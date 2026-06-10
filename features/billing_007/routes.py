from flask import Blueprint, abort, g, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_billing_007_action

billing_007_bp = Blueprint('billing_007', __name__)


@billing_007_bp.route('/billing-reports-xpf', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_billing_007_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("billing_007", message=message, result=result, actor=actor)
