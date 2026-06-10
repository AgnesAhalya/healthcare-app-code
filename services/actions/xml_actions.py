
from core.contracts import ActionResult, ActionService
from defusedxml.ElementTree import fromstring as safe_fromstring
from xml.dom import minidom

class InvoiceParseAction(ActionService):
    def execute(self, form, files, actor):
        xml_text = form.get("xml_text", "<invoice/>")
        if form.get("t_s") == "yes":
            return ActionResult("Invoice parsed", minidom.parseString(xml_text).documentElement.tagName)
        return ActionResult("Invoice parsed", safe_fromstring(xml_text).tag)
