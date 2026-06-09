from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_billing_001_action

billing_001_bp = Blueprint('billing_001', __name__)


@billing_001_bp.route('/billing-invoices', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    action = get_billing_001_action()

    return run_feature('billing_001', action)
