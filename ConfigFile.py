import json
from pathlib import Path
from functools import cached_property

from Validate import SchemaMismatchException, TypeMismatchException, assert_valid

INPUT_SCHEMA = {
	"questions": [
		{
			"name": str,
			"trials": [
				{
					"input": list[str],
					"output": list[str],
				}
			]
		}
	]
}

class ConfigFile:
	__path: Path
	questions: list[dict]
	valid: bool
	__error: str
	def __init__(self, file: str):
		self.valid = True
		self.__error = ""

		if file == "":
			self.error = "No file selected"
			return

		self.__path = Path(file)

		if not self.__path.exists():
			self.error = "File does not exist"
			return
		if not self.__path.is_file():
			self.error = "Path is not a file"
			return
		try:
			q = json.load(open(self.__path, "r"))
			assert_valid(q, INPUT_SCHEMA)
			self.questions = q["questions"]
		except json.decoder.JSONDecodeError:
			self.error = f"{self.__path.name} is not a valid JSON file"
			return
		except SchemaMismatchException as e:
			self.error = f"{self.__path.name} does not match the schema: {e}"
		except TypeMismatchException as e:
			self.error = f"Type mismatch in {self.__path.name}: {e}"

	@cached_property
	def path(self) -> str:
		"""The file path of the config file"""
		return self.__path.parent.as_posix()

	@cached_property
	def short_path(self) -> str:
		return (".../" if len(self.__path.parts) > 3 else "") + "/".join(self.__path.parts[-3:])

	@property
	def error(self) -> str:
		return self.__error

	@error.setter
	def error(self, value: str):
		self.valid = False
		self.__error = value