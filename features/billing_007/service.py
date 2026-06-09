FEATURE_NAME = 'Billing Report Alternate'


def get_page_model(actor=None):
    return {
        "feature": FEATURE_NAME,
        "actor": getattr(actor, "username", None),
        "status": "ready",
    }
