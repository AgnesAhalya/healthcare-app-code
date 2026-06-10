from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_billing_006_action
from flask import abort, g, render_template, request
billing_006_bp = Blueprint('billing_006', __name__)


@billing_006_bp.route('/billing-reports', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    actor = getattr(g, "current_session", None)
    action = get_billing_006_action()
    if request.method == "POST":
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)

    return run_feature('billing_006', action)
