from __future__ import annotations

from typing import Any

from services.feature_models import Field, FormSpec, TableSpec


def f(
    name,
    label,
    kind="text",
    value="",
    example="",
    required=False,
    options_from=None,
    option_value="",
    option_label="",
):
    return Field(
        name=name,
        label=label,
        kind=kind,
        value=value,
        example=example,
        required=required,
        options_from=options_from,
        option_value=option_value,
        option_label=option_label,
    )


def form(title, fields, action="default", submit="Submit", enctype=None, c2f=True):
    return FormSpec(
        title=title,
        action=action,
        submit=submit,
        enctype=enctype,
        c2f=c2f,
        fields=fields,
    )


def table(title, data_key, columns):
    return TableSpec(
        title=title,
        data_key=data_key,
        columns=columns,
    )


def _row_to_dict(row: Any) -> Any:
    if row is None:
        return []

    if isinstance(row, dict):
        return row

    try:
        return dict(row)
    except Exception:
        return {"value": row}


def _normalize(value: Any) -> Any:
    if value is None:
        return []

    if isinstance(value, (str, int, float, bool)):
        return [{"value": value}]

    if isinstance(value, dict):
        return [value]

    if isinstance(value, (list, tuple)):
        return [_row_to_dict(v) for v in value]

    try:
        return [_row_to_dict(value)]
    except Exception:
        return [{"value": repr(value)}]