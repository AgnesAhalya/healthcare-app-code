from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Callable
from flask import g, redirect, render_template, request


@dataclass(frozen=True)
class PageAction:
    name: str
    service: Any
    message: str


@dataclass(frozen=True)
class PageContext:
    name: str
    reader: Callable[[Any], Any]


def _current_actor():
    return getattr(g, "current_session", None)


def _normalize(value):
    if value is None:
        return []
    if isinstance(value, dict):
        return [value]
    if isinstance(value, (list, tuple)):
        return [dict(v) if not isinstance(v, dict) else v for v in value]
    try:
        return [dict(value)]
    except Exception:
        return [{"value": value}]


def render_feature_page(title: str, actions: dict[str, PageAction], contexts: list[PageContext]):
    """Legacy compatibility wrapper for older feature controllers.

    New feature routes use `services.feature_registry.run_feature`. This helper
    still renders a functional page if a future route calls it.
    """
    message = None
    result = None
    actor = _current_actor()

    if request.method == "POST" and actions:
        action_name = request.form.get("action") or "default"
        action = actions.get(action_name) or actions.get("default")
        if action is not None:
            action_result = action.service.execute(request.form, request.files, actor)
            message = action_result.message or action.message
            result = _normalize(action_result.payload)
            if action_result.redirect_to:
                return redirect(action_result.redirect_to)

    data = {ctx.name: _normalize(ctx.reader(actor)) for ctx in contexts}
    tables = [SimpleNamespace(title=k.replace("_", " ").title(), data_key=k, columns=[("value", "Value")]) for k in data]
    config = SimpleNamespace(title=title, description="Healthcare workflow page.", forms=[], tables=tables, result_label="Result")
    return render_template("feature_page.html", config=config, message=message, result=result, data=data)
