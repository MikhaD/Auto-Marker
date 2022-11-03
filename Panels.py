from tkinter import BooleanVar, Frame, Tk, Menu
from tkinter import filedialog as fd
from typing import Callable
from ConfigFile import ConfigFile
import os

from Settings import SETTINGS, FILE_TYPES
from Widgets import Button, Details, FileWidget, Heading, Text, CheckBoxPanel

class Window(Tk):
	padding = 10
	inset = 150
	def __init__(self, title: str):
		super().__init__()
		self.title(title)
		width = self.winfo_screenwidth()
		height = self.winfo_screenheight()
		# in case the OS doesn't support zoomed window
		self.geometry(f"{width-Window.inset*2}x{height-Window.inset*2}+{Window.inset}+{Window.inset//2}")
		self.wm_state("zoomed")
		self.protocol('WM_DELETE_WINDOW', self.on_exit)

		# menu
		menu = Menu(self)
		self.config(menu=menu)

		file_menu = Menu(menu, tearoff=False)
		menu.add_cascade(label="File", menu=file_menu)
		for file_type, var in SETTINGS.default.accepted_file_extensions.items():
			file_menu.add_checkbutton(label=file_type, command=self.__test, variable=BooleanVar(value=var))

		theme_menu = Menu(menu, tearoff=False)
		menu.add_cascade(label="Theme", menu=theme_menu)
		for theme in SETTINGS.themes:
			theme_menu.add_command(label=theme)

	def on_exit(self):
		SETTINGS.save_to("settings.json")
		self.destroy()
		exit(0)

	def __test(self):
		print("test")

class ControlsFrame(Frame):
	"""The control panel for the program to the left of the output window"""
	def __init__(self, master: Tk, config_file: ConfigFile | None = None):
		super().__init__(master, bg=SETTINGS.theme.bg_0, width=200)
		Heading(self, text="AUTOMATIC MARKER").pack(anchor="n", pady=Window.padding)
		if config_file is None:
			self.initial_controls = InitialConfig(self, self.on_choose)
			self.initial_controls.pack(anchor="n", pady=Window.padding)

		self.controls = Controls(self, config_file)

		self.pack(side="left", fill="both", expand=True)

	def on_choose(self, f: ConfigFile):
		self.controls.set_config_file(f)
		self.controls.pack(anchor="n", fill="both", expand=True)


class InitialConfig(Frame):
	on_choose: Callable
	def __init__(self, master: Tk | Frame, on_choose: Callable):
		super().__init__(master, bg=SETTINGS.theme.bg_0)

		self.on_choose = on_choose

		Heading(self, "CONFIGURATION FILE", 2).pack(anchor="n", pady=Window.padding)
		Text(self, f"Choose a configuration file to specify the files to compile and check and the inputs & expected outputs. If you run this script in a directory containing a file called {SETTINGS.default.config_file} it will be loaded automatically.").pack(anchor="n")
		Button(self, text="CHOOSE", command=self.choose_config).pack(anchor="n", pady=Window.padding)





	def choose_config(self):
		# open a tkinter file dialog asking for a json file
		file_path = fd.askopenfilename(initialdir="./", title="Select Automarker configuration file",filetypes=(("json files","*.json"),("all files","*.*")))
		file = ConfigFile(file_path)
		if file.valid:
			self.pack_forget()
			self.on_choose(file)
		else:
			print(file.error)

	def choose_different_config(self):
		self.choose_config()

class Controls(Frame):
	_config_file: ConfigFile
	def __init__(self, master: Tk | Frame, config_file: ConfigFile | None = None):
		super().__init__(master, bg=SETTINGS.theme.bg_0)

		Heading(self, "Choose Files To Mark", 2).pack(anchor="n")
		Text(self, "The files below are the ones the automarker will be trying to mark. A green check mark means the file has been found. A red X means the file could not be found. Click on a name to choose a file, or click the CHOOSE button to pick a directory to look for the files in. The directory containing the marking inputs will be used by default.").pack(anchor="n")

		self.files = Frame(self, bg=SETTINGS.theme.bg_0)
		self.files.pack(anchor="n", pady=Window.padding)

		d = Details(self, "CONFIGURATION FILE", self, level=2, open=True)
		d.pack(anchor="n", fill="x", pady=Window.padding)
		d.set_body(Frame(d))
		Text(d.body, "Current configuration file:").pack(anchor="n")
		Button(d.body, text="CHOOSE", command=self.choose_config).pack(anchor="n", pady=Window.padding)

		self.answer_types = CheckBoxPanel(self, list(FILE_TYPES.keys()), list(FILE_TYPES.values()))

		if config_file:
			self.set_config_file(config_file)
			self.pack(anchor="n", fill="both", expand=True)

	def choose_config(self):
		file_path = fd.askopenfilename(initialdir="./", title="Select Automarker configuration file",filetypes=(("json files","*.json"),("all files","*.*")))
		file = ConfigFile(file_path)
		if not file.valid:
			print(file.error)

	def set_config_file(self, file: ConfigFile):
		self._config_file = file
		for child in self.files.winfo_children():
			child.destroy()
		self.populate_files_list(file.question_names)

	def populate_files_list(self, files: tuple[str, ...]):
		for name in files:
			FileWidget(self.files, name, 7, is_found=self.check_exists(name)).pack(anchor="n", padx=Window.padding, pady=Window.padding/2)

	def check_exists(self, name: str) -> bool:
		files = {i.lower() for i in os.listdir(self._config_file.directory)}
		for extension in SETTINGS.default.accepted_file_extensions:
			if f"{name.lower()}.{extension}" in files:
				return True
		return False
		# return os.path.exists(os.path.join(self._config_file.directory, name))