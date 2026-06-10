
from core.contracts import ActionResult, ActionService
from db.repositories import ContentRepository
import html
class BannerCreateAction(ActionService):
    def __init__(self, content: ContentRepository | None = None):
        self.content = content or ContentRepository()
    def execute(self, form, files, actor):
        body = form.get("banner_text", "")
        return ActionResult("Banner created", self.content.create_banner(form.get("title", ""), html.escape(body,quote=False)))

class BannerListReader:
    def __init__(self, content: ContentRepository | None = None):
        self.content = content or ContentRepository()
    def read(self, actor):
        return self.content.list_banners()

class BannerPreviewAction(ActionService):
    def execute(self, form, files, actor):
        body = form.get("banner_text", "")
        return ActionResult("Preview generated", html.escape(body))