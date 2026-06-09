from flask import Blueprint
from services.access_control import require_role
from services.feature_registry import run_feature

billing_003_bp = Blueprint('billing_003', __name__)


@billing_003_bp.route('/billing-patient-view', methods=['GET'])
@require_role('billing_staff')
def feature_page():
    return run_feature('billing_003')