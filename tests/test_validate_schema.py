"""
>>> import Validate
>>> Validate.validate_schema({"a": 1}, {"a": int})
True
>>> Validate.validate_schema({"a": True}, {"a": int})
False
>>> Validate.validate_schema({"b": True}, {"a": bool})
False
>>> Validate.validate_schema({"b": [True, False]}, {"b": list[bool]})
True
>>> Validate.validate_schema({"b": {"c": 3}}, {"b": {"c": int}})
True
>>> Validate.validate_schema({"b": {"c": 3, "d": []}}, {"b": {"c": int, "d": list}})
True
>>> Validate.validate_schema({"b": {"c": 3, "d": [5, 6]}}, {"b": {"c": int, "d": list[str]}})
False
>>> Validate.validate_schema({"b": {"c": 3, "d": [{"f": "hi"}, {"f": "bye"}]}}, {"b": {"c": int, "d": list[str]}})
False
>>> Validate.validate_schema({"b": {"c": 3, "d": [{"f": "hi"}, {"f": "bye"}]}}, {"b": {"c": int, "d": {"f": str}}})
True
"""