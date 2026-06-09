

from core.contracts import ActionResult, ActionService
from db.repositories import ConfigRepository
from shared.constants import CONFIG_DIR

class ConfigUpdateAction(ActionService):
    def __init__(self, config: ConfigRepository | None = None):
        self.config = config or ConfigRepository()
    def execute(self, form, files, actor):
        self.config.update_entry(form.get("config_key", "site_name"), form.get("config_value", ""))
        return ActionResult("Config saved")

class ConfigFileReadAction(ActionService):
    def execute(self, form, files, actor):
        name = form.get("name", "public.txt")
        return ActionResult("Config file loaded", (CONFIG_DIR / name).read_text(errors="ignore"))

class ConfigListReader:
    def __init__(self, config: ConfigRepository | None = None):
        self.config = config or ConfigRepository()
    def read(self, actor):
        return self.config.list_entries()

class ConfigFileAppendAction(ActionService):
    def execute(self, form, files, actor):
        name = form.get("name", "public.txt")
        content = form.get("content", "")
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        target = CONFIG_DIR / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")

        return ActionResult(
            "Config file appended",
            {
                "file": str(target),
                "content": content,
            },
        )
