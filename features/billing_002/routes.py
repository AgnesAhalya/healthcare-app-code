from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

billing_002_bp = Blueprint('billing_002', __name__)


@billing_002_bp.route('/billing-invoices-sec', methods=['GET', 'POST'])
@require_role('billing_staff')
def feature_page():
    return run_feature('billing_002')
