from types import GenericAlias, UnionType
from typing import Any, Union, _UnionGenericAlias  # type: ignore

class InvalidSchema(Exception):
	"""Raised when a schema is invalid."""
	pass

class MessageException(Exception):
	"""Raised when a message is invalid."""
	message: str
	def __init__(self, message: str) -> None:
		super().__init__(message)
		self.message = message

	def __str__(self) -> str:
		return self.message

class TypeMismatchException(MessageException):
	"""Raised when a value doesn't match a type."""
	pass

class SchemaMismatchException(MessageException):
	"""Raised when a value doesn't match a schema."""
	pass


def assert_is_type(value: Any, test_type: Union[type, GenericAlias, UnionType]):
	"""
	Check if a value is of a certain type or parameterized generic type. Returns `True` if the value is of the given type, and `False` otherwise. Type can be any primitive python type, `int`, `float`, `bool`, or `str`, or any of the raw basic data structures, `list`, `tuple`, `dict`, or `set`.

	The main use for this function comes from its support for parameterized generic types. For example, `is_type([1, 2, 3], list[int])` returns `True`, and `is_type([1, 2, 3], list[str])` returns `False`. This is useful for validating lists of objects, for example.
	"""
	if type(value) == test_type: return True
	if type(test_type) in (_UnionGenericAlias, UnionType):
		types = getattr(test_type, "__args__", None)
		for t in types:
			if assert_is_type(value, t): return True
		raise TypeMismatchException(f"{value} is type {type(value)} which does not match {types}")
	if type(value) not in (tuple, set, list, dict):
		raise TypeMismatchException(f"{value} is type {type(value)} which does not match {test_type}")
	base_type = getattr(test_type, "__origin__", False)
	type_args = getattr(test_type, "__args__", [])
	if not base_type or type(value) != base_type:
		raise TypeMismatchException(f"{value} is type {type(value)} which does not match {base_type}")
	if base_type == tuple:
		if len(type_args) != len(value):
			raise TypeMismatchException(f"Tuple {value} with {len(value)} elements cannot match tuple with {len(type_args)} elements")
		for v, t in zip(value, getattr(test_type, "__args__")):
			assert_is_type(v, t)
		return True
	if base_type == dict:
		for v in value.values():
			for t in type_args:
				if assert_is_type(v, t): break
			else:
				raise TypeMismatchException(f"Value {v} does not match any of the types {type_args}")
		return True
	# if base_type == list or base_type == set:
	for v in value:
		for t in type_args:
			if assert_is_type(v, t): break
		# for else triggers the else if the for loop ends without breaking
		else:
			raise TypeMismatchException(f"Value {v} does not match any of the types {type_args}")
	return True

def assert_valid(obj: Any, schema: Any):
	"""
	Check if a dict or list matches a schema. Rases an error if the object doesn't match the schema.
	"""
	if isinstance(schema, (int, float, str, bool)) or schema is None:
		if obj == schema: return True
		raise SchemaMismatchException(f"Expected literal {schema}, got {obj}")
	if isinstance(schema, (type, GenericAlias, UnionType, _UnionGenericAlias)):
		assert_is_type(obj, schema)
		return True
		# raise SchemaMatchException(f"Expected type {schema}, got {type(obj)}")
	if type(obj) != type(schema):
		raise SchemaMismatchException(f"Expected {type(schema)}, got {type(obj)}")
	if type(schema) == dict:
		non_literals = 0
		general_key = False
		for key in schema:
			if isinstance(key, str):
				if key not in obj: raise SchemaMismatchException(f"Missing key {key}")
				assert_valid(obj[key], schema[key])
			elif key == str:
				if general_key: raise InvalidSchema("Multiple general keys in schema")
				general_key = True
				for k in obj:
					if k not in schema:
						assert_valid(obj[k], schema[key])
						non_literals += 1
		# True is the same as 1, False is the same as 0
		if len(obj) - non_literals != len(schema) - general_key: raise SchemaMismatchException("Extra keys in object")

	elif type(schema) == list:
		for i in obj:
			for sub_schema in schema:
				if assert_valid(i, sub_schema):
					break
			# for else triggers the else if the for loop ends without breaking
			else: raise SchemaMismatchException(f"Object {i} doesn't match any schema")
	return True