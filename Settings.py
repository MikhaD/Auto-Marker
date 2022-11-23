import json
from typing import Any
import os

__all__ = ["SETTINGS"]


class Settings:
	FILE_TYPES = {
		"Java": "java",
		"Python": "py"
	}
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Settings, cls).__new__(cls)
		return cls.__instance

	def __init__(self, file: str):
		try:
			with open(file, "r") as f:
				data = json.load(f)
			self.default = Defaults(data["default"])
			self.themes = {i: Theme(i, data["style"]["themes"][i]) for i in data["style"]["themes"]}
			if "theme" in data["style"] and data["style"]["theme"] in self.themes:
				self.theme = self.themes[data["style"]["theme"]]
			else:
				self.theme = self.themes[self.default.theme]
			self.font = Font(data["font"])
		except Exception as e:
			self.default = Defaults()
			self.themes = {self.default.theme: Theme(self.default.theme)}
			self.font = Font()
			self.theme = self.themes[self.default.theme]
			print("Failed to load settings file, using defaults", e)

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
	SCRIPT_PATHS = {}
	TIMEOUT = 1
	THEME = "vula-dark"
	CONFIG_FILE = "inputs.json"
	ACCEPTED_FILE_EXTENSIONS = {Settings.FILE_TYPES[i]: True for i in Settings.FILE_TYPES}

	script_paths: dict[str, str]
	accepted_file_extensions: dict[str, bool]
	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Defaults, cls).__new__(cls)
		return cls.__instance

	def __init__(self, obj: dict | None = None):
		if obj != None:
			self.theme = obj["theme"]
			self.config_file = obj["config-file"]
			self.timeout = obj["timeout"]
			if not os.path.exists(self.config_file):
				self.config_file = Defaults.CONFIG_FILE
				self.script_paths = Defaults.SCRIPT_PATHS
			else:
				self.script_paths = obj["script-paths"]
			self.accepted_file_extensions = {Settings.FILE_TYPES[i]: Settings.FILE_TYPES[i] in obj["accepted-file-extensions"] for i in Settings.FILE_TYPES}
		else:
			# default values
			self.theme = Defaults.THEME
			self.config_file = Defaults.CONFIG_FILE
			self.timeout = Defaults.TIMEOUT
			self.script_paths = Defaults.SCRIPT_PATHS
			self.accepted_file_extensions = Defaults.ACCEPTED_FILE_EXTENSIONS

	def obj(self) -> dict:
		return {
			"theme": self.theme,
			"config-file": self.config_file,
			"script-paths": self.script_paths,
			"timeout": self.timeout,
			"accepted-file-extensions": [i for i in self.accepted_file_extensions if self.accepted_file_extensions[i]]
		}


class Theme:
	BG_0 = "#1F2225"
	BG_1 = "#0E0E0E"
	BG_2 = "#31353B"
	BG_3 = "#434950"
	FG_0 = "#ffffff"
	FG_1 = "#dddddd"
	FG_2 = "#444444"
	ACCENT_0 = "#135273"
	ACCENT_1 = "#155A7E"
	RED = "#FF0000"
	GREEN = "#00FF00"
	YELLOW = "#FFFF00"

	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Theme, cls).__new__(cls)
		return cls.__instance

	def __init__(self, name: str, obj: dict | None = None):
		self.name = name
		if obj != None:
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
		else:
			# default values
			self.bg_0 = Theme.BG_0
			self.bg_1 = Theme.BG_1
			self.bg_2 = Theme.BG_2
			self.bg_3 = Theme.BG_3
			self.fg_0 = Theme.FG_0
			self.fg_1 = Theme.FG_1
			self.fg_2 = Theme.FG_2
			self.accent_0 = Theme.ACCENT_0
			self.accent_1 = Theme.ACCENT_1
			self.red = Theme.RED
			self.green = Theme.GREEN
			self.yellow = Theme.YELLOW

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

	@property
	def bg_disabled(self) -> str:
		return self.fg_2

	@property
	def fg_disabled(self) -> str:
		return self.fg_1


class Font:
	REGULAR = "Arial"
	CODE = "Consolas"

	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(Font, cls).__new__(cls)
		return cls.__instance

	def __init__(self, obj: dict | None = None):
		if obj != None:
			self.regular = obj["regular"]
			self.code = obj["code"]
			self.size = FontSize(obj["size"])
		else:
			# default values
			self.regular = Font.REGULAR
			self.code = Font.CODE
			self.size = FontSize()

	def obj(self) -> dict:
		return {"regular": self.regular, "code": self.code, "size": self.size.obj()}


class FontSize:
	REGULAR = 12
	CODE = 12
	H1 = 24
	H2 = 18
	H3 = 16
	BUTTON = 14

	def __new__(cls, *args: Any, **kwargs: Any):
		if not hasattr(cls, 'instance'):
			cls.__instance = super(FontSize, cls).__new__(cls)
		return cls.__instance

	def __init__(self, obj: dict | None = None):
		if obj != None:
			self.regular = obj["regular"]
			self.code = obj["code"]
			self.h1 = obj["h1"]
			self.h2 = obj["h2"]
			self.h3 = obj["h3"]
			self.button = obj["button"]
		else:
			# default values
			self.regular = FontSize.REGULAR
			self.code = FontSize.CODE
			self.h1 = FontSize.H1
			self.h2 = FontSize.H2
			self.h3 = FontSize.H3
			self.button = FontSize.BUTTON


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