import json
from typing import Any

__all__ = ["SETTINGS", "FILE_TYPES"]

FILE_TYPES = {
	"Java": "java",
	"Python": "py"
}

class Settings:
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Settings, cls).__new__(cls)
		return cls.__instance

	def __init__(self, file: str):
		with open(file, "r") as f:
			data = json.load(f)
		self.default = Defaults(data["default"])
		self.themes = {i: Theme(i, data["style"]["themes"][i]) for i in data["style"]["themes"]}
		if "theme" in data["style"] and data["style"]["theme"] in self.themes:
			self.theme = self.themes[data["style"]["theme"]]
		else:
			self.theme = self.themes[self.default.theme]
		self.font = Font(data["font"])

	def obj(self) -> dict:
		return {
			"default": self.default.obj(),
			"style": {"theme": self.theme.name, "themes": {i: self.themes[i].obj() for i in self.themes}},
			"font": self.font.obj()
		}
	def __repr__(self) -> str:
		return json.dumps(self.obj(), indent="\t")

	def save_to(self, file: str):
		f = open(file, "w")
		f.write(self.__repr__())
		f.close()


class Defaults:
	theme: str
	config_file: str
	accepted_file_extensions: dict[str, bool]
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Defaults, cls).__new__(cls)
		return cls.__instance

	def __init__(self, obj: dict):
		self.theme = obj["theme"]
		self.config_file = obj["config-file"]
		self.accepted_file_extensions = {i: i in obj["accepted-file-extensions"] for i in FILE_TYPES}

	def obj(self) -> dict:
		return {
			"theme": self.theme,
			"config-file": self.config_file,
			"accepted-file-extensions": [i for i in self.accepted_file_extensions if self.accepted_file_extensions[i]]}


class Theme:
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Theme, cls).__new__(cls)
		return cls.__instance

	def __init__(self, name: str, obj: dict):
		self.name = name
		self.bg_0 = obj["bg-0"]
		self.bg_1 = obj["bg-1"]
		self.bg_2 = obj["bg-2"]
		self.bg_3 = obj["bg-3"]
		self.fg_0 = obj["fg-0"]
		self.fg_1 = obj["fg-1"]
		self.fg_2 = obj["fg-2"]
		self.accent_0 = obj["accent-0"]
		self.accent_1 = obj["accent-1"]
		self.red = obj["red"]
		self.green = obj["green"]
		self.yellow = obj["yellow"]

	def obj(self) -> dict:
		return {
			"bg-0": self.bg_0,
			"bg-1": self.bg_1,
			"bg-2": self.bg_2,
			"bg-3": self.bg_3,
			"fg-0": self.fg_0,
			"fg-1": self.fg_1,
			"fg-2": self.fg_2,
			"accent-0": self.accent_0,
			"accent-1": self.accent_1,
			"red": self.red,
			"green": self.green,
			"yellow": self.yellow
		}


class Font:
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Font, cls).__new__(cls)
		return cls.__instance

	def __init__(self, obj: dict):
		self.regular = obj["regular"]
		self.code = obj["code"]
		self.size = FontSize(obj["size"])

	def obj(self) -> dict:
		return {"regular": self.regular, "code": self.code, "size": self.size.obj()}


class FontSize:
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(FontSize, cls).__new__(cls)
		return cls.__instance

	def __init__(self, obj: dict):
		self.regular = obj["regular"]
		self.code = obj["code"]
		self.h1 = obj["h1"]
		self.h2 = obj["h2"]
		self.h3 = obj["h3"]
		self.button = obj["button"]

	def obj(self) -> dict:
		return {
			"regular": self.regular,
			"code": self.code,
			"h1": self.h1,
			"h2": self.h2,
			"h3": self.h3,
			"button": self.button
		}

SETTINGS = Settings("settings.json")