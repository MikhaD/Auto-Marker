import json
from pathlib import Path

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
	path: Path
	questions: list[dict]
	question_names: tuple
	valid: bool
	__error: str
	def __init__(self, file: str):
		self.valid = True
		self.__error = ""

		if file == "":
			self.error = "No file selected"
			return

		self.path = Path(file)

		if not self.path.exists():
			self.error = "File does not exist"
			return
		if not self.path.is_file():
			self.error = "Path is not a file"
			return
		try:
			self.questions = json.load(open(self.path, "r"))
			assert_valid(self.questions, INPUT_SCHEMA)
			self.question_names = tuple((question["name"] for question in self.questions["questions"]))
		except json.decoder.JSONDecodeError:
			self.error = f"{self.path.name} is not a valid JSON file"
			return
		except SchemaMismatchException as e:
			self.error = f"{self.path.name} does not match the schema: {e}"
		except TypeMismatchException as e:
			self.error = f"Type mismatch in {self.path.name}: {e}"

	@property
	def error(self) -> str:
		return self.__error

	@error.setter
	def error(self, value: str):
		self.valid = False
		self.__error = value