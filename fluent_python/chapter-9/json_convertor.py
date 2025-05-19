import json
from datetime import date, datetime
from functools import singledispatch


@singledispatch
def to_json(obj):
    """Convert an object to a JSON string."""
    try:
        return json.dumps(obj)
    except TypeError:
        return json.dumps(str(obj))


@to_json.register
def _(obj: dict):
    return json.dumps(obj)


@to_json.register
def _(obj: list):
    return json.dumps(obj)


@to_json.register
def _(obj: datetime | date):
    return json.dumps(obj.isoformat())


@to_json.register
def _(obj: object):
    if hasattr(obj, "__dict__"):
        return json.dumps(obj.__dict__)
    else:
        return json.dumps(str(obj))
