from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_billing_007_action

billing_007_bp = Blueprint('billing_007', __name__)


@billing_007_bp.route('/billing-reports-xpf', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    action = get_billing_007_action()

    return run_feature('billing_007', action)
