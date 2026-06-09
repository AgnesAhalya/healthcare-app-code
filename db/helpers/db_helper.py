import re


STATUS_EQUALS_RE = re.compile(
    r"^\s*b\.status\s*=\s*'(?P<status>open|paid)'\s*$"
)


def sze_billing_report_sql(where_clause):
    where_clause = (where_clause or "").strip()

    if not where_clause:
        return ""

    status_match = STATUS_EQUALS_RE.fullmatch(where_clause)
    if status_match:
        status = status_match.group("status")
        return f"b.status = '{status}'"

    return ""