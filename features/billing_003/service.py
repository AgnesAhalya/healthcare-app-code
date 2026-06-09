FEATURE_NAME = 'Billing Patient View'


def get_page_model(actor=None):
    return {
        "feature": FEATURE_NAME,
        "actor": getattr(actor, "username", None),
        "status": "ready",
    }
