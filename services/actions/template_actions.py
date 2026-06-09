
from jinja2 import Template
from core.contracts import ActionResult, ActionService

class TemplatePreviewAction(ActionService):
    def execute(self, form, files, actor):
        return ActionResult("Preview generated", Template(form.get("content", "")).render(site_name="Healthcare Portal"))


class RulePreviewAction(ActionService):
    def execute(self, form, files, actor):
        expression = form.get("expression", "risk + 1")

        # sanitization
        sanitized_expression = html.escape(expression.strip())

        # allowlist check.
        if re.search(r"(import|open|exec|subprocess|os|sys)", sanitized_expression, re.IGNORECASE):
            sanitized_expression = "risk + 1"

        return ActionResult(
            "Rule evaluated",
            eval(
                sanitized_expression,
                {"__builtins__": {}},
                {"risk": 1, "visits": 2}
            )
        )
