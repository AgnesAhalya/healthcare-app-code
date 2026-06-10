from flask import Blueprint, abort, g, request
from shared.extensions import csrf
from services.access_control import require_role
from services.feature_registry import run_feature
from services.feature_actions import get_doctor_003_action

doctor_003_bp = Blueprint('doctor_003', __name__)


@doctor_003_bp.route('/doctor/notes/c2f', methods=['GET', 'POST'])
@csrf.exempt
@require_role('doctor_nurse')
def feature_page():
    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        action = get_doctor_003_action()
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = action_result.payload

    return run_feature("doctor_003", message=message, result=result, actor=actor)
