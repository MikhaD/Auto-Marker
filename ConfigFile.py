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
	question_names: tuple[str, ...]
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
			self.questions = json.load(open(self.__path, "r"))
			assert_valid(self.questions, INPUT_SCHEMA)
			self.question_names = tuple((question["name"] for question in self.questions["questions"]))
		except json.decoder.JSONDecodeError:
			self.error = f"{self.__path.name} is not a valid JSON file"
			return
		except SchemaMismatchException as e:
			self.error = f"{self.__path.name} does not match the schema: {e}"
		except TypeMismatchException as e:
			self.error = f"Type mismatch in {self.__path.name}: {e}"

	@cached_property
	def directory(self):
		return self.__path.parent.as_posix()

	@property
	def error(self) -> str:
		return self.__error

	@error.setter
	def error(self, value: str):
		self.valid = False
		self.__error = value