from flask import Blueprint, abort, g, request
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_006_action

patient_006_bp = Blueprint('patient_006', __name__)


@patient_006_bp.route('/outpatient/bills', methods=['GET', 'POST'])
@patient_006_bp.route('/outpatient/payments', methods=['GET', 'POST'])
@require_role('outpatient')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_patient_006_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("patient_006", message=message, result=result, actor=actor)
