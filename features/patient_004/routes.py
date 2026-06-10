from flask import Blueprint, abort, g, request
from shared.extensions import csrf
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_patient_004_action

patient_004_bp = Blueprint('patient_004', __name__)


@patient_004_bp.route('/maintainer/c2f', methods=['GET', 'POST'])
@csrf.exempt
@require_role('outpatient')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_patient_004_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("patient_004", message=message, result=result, actor=actor)
