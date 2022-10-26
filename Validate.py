from types import GenericAlias
from typing import Any, Union

def is_type(value: Any, test_type: Union[type, GenericAlias]):
	"""Check if a value is of a certain type or complex type."""
	if type(value) == test_type: return True
	if type(value) not in (tuple, set, list, dict): return False
	base_type = getattr(test_type, "__origin__", False)
	type_args = getattr(test_type, "__args__", [])
	if not base_type or type(value) != base_type: return False
	if base_type == tuple:
		if len(type_args) != len(value): return False
		for v, t in zip(value, getattr(test_type, "__args__")):
			if not is_type(v, t): return False
		return True
	if base_type == dict:
		for v in value.values():
			for t in type_args:
				if is_type(v, t): break
			else: return False
		return True
	for v in value:
		for t in type_args:
			if is_type(v, t): break
		# for else triggers the else if the for loop ends without breaking
		else: return False
	return True

def validate_schema(obj: Union[dict, list], schema: Union[dict, list]):
	"""
	Check if a dict or list matches a schema
	Limitation: Objects in lists need to all match the same schema.
	"""
	if type(obj) != type(schema): return False
	for key in schema:
		if key not in obj: return False
		if isinstance(schema[key], (type, GenericAlias)):
			if not is_type(obj[key], schema[key]):
				return False
			continue
		if type(obj[key]) is dict:
			if not validate_schema(obj[key], schema[key]):
				return False
		if type(obj[key]) is list:
			for i in obj[key]:
				if not validate_schema(i, schema[key][0]):
					return False
	return True

if __name__ == "__main__":
	obj = {
		"questions": [
			{
				"name": "test",
				"trials": [
					{
						"input": ["test"],
						"output": ["test"]
					}
				]
			}
		]
	}
	schema = {
		"questions": [
			{
				"name": str,
				"trials": [
					{
						"input": list[str],
						"output": list[str]
					}
				]
			}
		]
	}
	print(validate_schema(obj, schema))