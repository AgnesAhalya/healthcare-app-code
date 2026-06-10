FEATURE_NAME = 'Patient Payment Redirect'


def get_page_model(actor=None):
    return {
        "feature": FEATURE_NAME,
        "actor": getattr(actor, "username", None),
        "status": "ready",
    }
