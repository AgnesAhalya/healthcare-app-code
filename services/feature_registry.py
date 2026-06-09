from __future__ import annotations

from typing import Any

from flask import abort, g, render_template, request

from services.feature_config import FeatureConfig, get_feature_config
from services.feature_helpers import _normalize


ROLE_UI = {
    "outpatient": ("Patient Portal", "Outpatient care tasks", "🩺", "/outpatient/profile"),
    "inpatient": ("Patient Portal", "Inpatient profile access", "🏥", "/inpatient/profile"),
    "doctor_nurse": ("Clinical Workspace", "Doctor and nurse workflows", "🧑‍⚕️", "/doctor/employee-record"),
    "billing_staff": ("Billing Desk", "Patient billing and payments", "💳", "/billing-patient-view"),
    "role_manager": ("Role Manager Console", "User access administration", "🛡️", "/role-manager/roles"),
    "maintainer": ("Maintainer Console", "Site content and maintenance", "🛠️", "/maintainer/awareness"),
    "security_auditor": ("Security Audit Desk", "Monitoring and audit review", "🔎", "/auditor-audit"),
    "external_user": ("Partner Portal", "External customer record view", "🤝", "/external/records"),
}


MODULE_LABELS = {
    "appointment": "Appointments",
    "record": "Medical Records",
    "payment": "Payments",
    "bill": "Billing",
    "invoice": "Invoices",
    "report": "Reports",
    "role": "Access Control",
    "config": "Configuration",
    "banner": "Awareness Content",
    "backup": "Backup Operations",
    "audit": "Audit Collection",
    "log": "Audit Logs",
    "api": "API Credentials",
    "employee": "Employee Records",
    "notes": "Clinical Notes",
    "external": "Partner Records",
}


def _module_label(feature_id: str) -> str:
    for token, label in MODULE_LABELS.items():
        if token in feature_id:
            return label

    return "Healthcare Workflow"


def _caption_for_key(key: str) -> str:
    readable = key.replace("_", " ").title()

    if key in {
        "bills",
        "payments",
        "records",
        "appointments",
        "patients",
        "roles",
        "users",
        "entries",
        "events",
        "banners",
    }:
        return f"{readable} currently visible"

    return f"{readable} loaded"


def _build_ui(
    config: FeatureConfig,
    data: dict[str, Any],
    actor: Any,
) -> dict[str, Any]:
    role_label, role_caption, role_icon, home_href = ROLE_UI.get(
        config.role,
        ("Healthcare Workspace", "Care operations", "🏥", "/login"),
    )

    metrics = []

    for key, rows in list(data.items())[:4]:
        metrics.append(
            {
                "label": key.replace("_", " ").title(),
                "value": len(rows),
                "caption": _caption_for_key(key),
            }
        )

    if not metrics:
        metrics.append(
            {
                "label": "Actions",
                "value": len(config.forms),
                "caption": "Available workflow actions",
            }
        )
        metrics.append(
            {
                "label": "Tables",
                "value": len(config.tables),
                "caption": "Live data views",
            }
        )

    actor_label = actor.user_id if actor is not None else "Active session"

    return {
        "role_label": role_label,
        "role_caption": role_caption,
        "role_icon": role_icon,
        "home_href": home_href,
        "module_label": _module_label(config.feature_id),
        "metrics": metrics,
        "actor_label": actor_label,
        "empty_message": f"No {config.title.lower()} records are available for this signed-in workspace yet.",
    }


def run_feature(
    feature_id: str,
    action: Any = None,
):
    config = get_feature_config(feature_id)

    if config is None:
        abort(404)

    message = None
    result = None
    actor = getattr(g, "current_session", None)

    if request.method == "POST":
        if action is None:
            abort(400)

        action_result = action.execute(request.form, request.files, actor)
        message = action_result.message
        result = _normalize(action_result.payload)

    data = {}

    for key, reader in config.readers.items():
        try:
            data[key] = _normalize(reader.read(actor))
        except Exception as exc:
            data[key] = [{"error": str(exc)}]

    return render_template(
        "feature_page.html",
        feature=config,
        config=config,
        message=message,
        result=result,
        data=data,
        ui=_build_ui(config, data, actor),
    )