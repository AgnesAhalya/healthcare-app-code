from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_billing_004_action

billing_004_bp = Blueprint('billing_004', __name__)


@billing_004_bp.route('/billing-payments', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    action = get_billing_004_action()

    return run_feature('billing_004', action)
