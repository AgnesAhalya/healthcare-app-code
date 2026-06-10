from datetime import datetime

DB_DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def parse_appointment_datetime(appointment_datetime):
    if isinstance(appointment_datetime, datetime):
        return appointment_datetime.replace(second=0, microsecond=0)

    if not appointment_datetime:
        raise ValueError("appointment_datetime is required")

    value = str(appointment_datetime).strip()

    accepted_formats = [
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M",
        "%d.%m.%Y, %H:%M",
        "%d.%m.%Y %H:%M",
    ]

    for fmt in accepted_formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    raise ValueError(f"Invalid appointment_datetime format: {value}")


def format_appointment_datetime_for_db(appointment_datetime):
    return parse_appointment_datetime(appointment_datetime).strftime(
        DB_DATETIME_FORMAT
    )