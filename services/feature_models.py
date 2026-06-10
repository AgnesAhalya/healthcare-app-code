from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Field:
    name: str
    label: str
    kind: str = "text"
    value: str = ""
    example: str = ""
    required: bool = False
    options_from: str | None = None
    option_value: str = ""
    option_label: str = ""


@dataclass(frozen=True)
class FormSpec:
    title: str
    action: str = "default"
    submit: str = "Submit"
    method: str = "post"
    enctype: str | None = None
    c2f: bool = True
    fields: list[Field] = field(default_factory=list)


@dataclass(frozen=True)
class TableSpec:
    title: str
    data_key: str
    columns: list[tuple[str, str]]


@dataclass(frozen=True)
class FeatureConfig:
    feature_id: str
    title: str
    role: str
    description: str
    readers: dict[str, Any] = field(default_factory=dict)
    forms: list[FormSpec] = field(default_factory=list)
    tables: list[TableSpec] = field(default_factory=list)
    result_label: str = "Result"