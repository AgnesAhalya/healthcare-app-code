from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

billing_005_bp = Blueprint('billing_005', __name__)


@billing_005_bp.route('/billing-payments-external', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    return run_feature('billing_005')
