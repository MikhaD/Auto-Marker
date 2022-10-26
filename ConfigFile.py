import json
import os
from pathlib import Path

class ConfigFile:
	path: str
	file_name: str
	__error: str
	valid: bool
	def __init__(self, path: str):
		self.valid = True
		self.path = os.path.normpath(path)
		self.file_name = os.path.basename(path)
		self.path = path

	def __parse(self) -> None:
		if not os.path.exists(self.path):
			self.error = f"File {self.path} does not exist."
			return
		if not os.path.isfile(self.path):
			self.error = f"{self.file_name} is not a file."
			return
		try:
			with open(self.path, "r") as f:
				data = json.load(f)
			self.__validate_schema(data)
		except json.JSONDecodeError:
			self.error = f"File {self.file_name} is not a valid JSON file."
			return
		except Exception as e:
			self.error = f"Error parsing file {self.file_name}: {e}"

	def __validate_schema(self, data: dict) -> None:
		base_error = f"{self.file_name} has the incorrect format. "
		if "questions" not in data:
				self.error = base_error + "Top level should contain the questions key."
				return
		if type(data["questions"]) is not list:
			self.error = base_error + "The questions key should contain a list."
			return
		for question in data["questions"]:
			if "name" not in question or type(question["name"]) is not str:
				self.error = base_error + "Each question should contain a name key with a string value."
				return
			if "trials" not in question or type(question["trials"]) is not list:
				self.error = base_error + "Each question should contain a trials key with a list value."
				return
			for trial in question["trials"]:


	@property
	def error(self) -> str:
		return self.__error

	@error.setter
	def error(self, value: str):
		self.valid = False
		self.__error = value

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