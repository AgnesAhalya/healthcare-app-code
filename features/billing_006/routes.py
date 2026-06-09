from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_billing_006_action
billing_006_bp = Blueprint('billing_006', __name__)


@billing_006_bp.route('/billing-reports', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    action = get_billing_006_action("default")
    return run_feature('billing_006',action=action)
