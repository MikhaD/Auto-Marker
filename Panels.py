import tkinter as tk
from tkinter import filedialog as fd
from typing import Callable
from ConfigFile import ConfigFile
import os
from pathlib import Path
from Marker import Marker

from Settings import SETTINGS
from Widgets import Button, Details, FileWidget, Heading, Text, CheckBoxPanel

class Window(tk.Tk):
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
		# menu = Menu(self)
		# self.config(menu=menu)

		# file_menu = Menu(menu, tearoff=False)
		# menu.add_cascade(label="File", menu=file_menu)
		# for file_type, var in SETTINGS.default.accepted_file_extensions.items():
		# 	file_menu.add_checkbutton(label=file_type, command=self.__test, variable=BooleanVar(value=var))

		# theme_menu = Menu(menu, tearoff=False)
		# menu.add_cascade(label="Theme", menu=theme_menu)
		# for theme in SETTINGS.themes:
		# 	theme_menu.add_command(label=theme)

	# def __test(self):
	# 	print("test")

	def on_exit(self):
		SETTINGS.save_to("settings.json")
		self.destroy()
		exit(0)

class ControlsFrame(tk.Frame):
	"""The control panel for the program to the left of the output window"""
	def __init__(self, master: tk.Tk, config_file: ConfigFile | None, marker: Marker):
		super().__init__(master, bg=SETTINGS.theme.bg_0, width=200)
		Heading(self, text="AUTOMATIC MARKER").pack(anchor="n", pady=Window.padding)
		if config_file is None:
			self.initial_controls = InitialConfig(self, self.on_choose)
			self.initial_controls.pack(anchor="n", pady=Window.padding, padx=100)

		self.controls = Controls(self, config_file, marker)

		self.pack(side="left", fill="both", expand=True)

	def on_choose(self, f: ConfigFile):
		self.controls.set_config_file(f)
		self.controls.pack(anchor="n", fill="both", padx=100)


class InitialConfig(tk.Frame):
	on_choose: Callable
	def __init__(self, master: tk.Tk | tk.Frame, on_choose: Callable):
		super().__init__(master, bg=SETTINGS.theme.bg_0)

		self.on_choose = on_choose

		Heading(self, "CONFIGURATION FILE", 2).pack(anchor="n", pady=Window.padding)
		Text(self, f"Choose a configuration file to specify the files to compile and check and the inputs & expected outputs. If you run this script in a directory containing a file called {SETTINGS.default.CONFIG_FILE} it will be loaded automatically.").pack(anchor="n")
		Button(self, text="CHOOSE", command=self.choose_config).pack(anchor="n", pady=Window.padding)

	def choose_config(self):
		# open a tkinter file dialog asking for a json file
		file_path = fd.askopenfilename(initialdir="./", title="Select Automarker configuration file",filetypes=(("json files","*.json"),("all files","*.*")))
		file = ConfigFile(file_path)
		if file.valid:
			self.pack_forget()
			self.on_choose(file)
			SETTINGS.default.config_file = file.path
		else:
			print(file.error)

	def choose_different_config(self):
		self.choose_config()

class Controls(tk.Frame):
	_config_file: ConfigFile
	file_widgets: list[FileWidget]
	marker: Marker
	def __init__(self, master: tk.Tk | tk.Frame, config_file: ConfigFile | None, marker: Marker):
		super().__init__(master, bg=SETTINGS.theme.bg_0)
		self.file_widgets = []
		self.marker = marker

		Heading(self, "Choose Files To Mark", 2).pack(anchor="n")
		Text(self, "The files below are the ones the automarker will be trying to mark. A green check mark means the file has been found. A red X means the file could not be found. Click on a name to choose a file, or click the CHOOSE button to pick a directory to look for the files in. The directory containing the marking inputs will be used by default.").pack(anchor="n")

		self.files = tk.Frame(self, bg=SETTINGS.theme.bg_0)
		self.files.pack(anchor="n", pady=Window.padding)

		self.mark_btn = Button(self, "MARK", self.mark, True)
		self.mark_btn.pack(anchor="n")

		d = Details(self, "Accepted File Types", level=2, open=True)
		d.pack(anchor="n", fill="x")
		self.answer_types = CheckBoxPanel(d, list(SETTINGS.FILE_TYPES.keys()), list(SETTINGS.FILE_TYPES.values()), command=self.update_exists)
		d.set_body(self.answer_types)

		d = Details(self, "CONFIGURATION FILE", level=2, open=False)
		d.pack(anchor="n", fill="x", pady=Window.padding)
		d.set_body(tk.Frame(d))
		cct = tk.Frame(d.body, bg=SETTINGS.theme.bg_0)
		cct.pack(anchor="n")
		Text(cct, "Current configuration file:").pack(side="left")

		self.current_config_text = Text(cct, "", code=True, bg=SETTINGS.theme.bg_1)
		self.current_config_text.pack(side="left")
		Button(d.body, text="CHOOSE ANOTHER", command=self.choose_config).pack(anchor="n", pady=Window.padding)

		if config_file:
			self.set_config_file(config_file)
			self.pack(anchor="n", fill="both", expand=True)

	def mark(self):
		self.mark_btn.toggle_disabled(True)

		self.marker.mark(self._config_file, {file_widget.name.lower(): file_widget.file_path for file_widget in self.file_widgets if file_widget.is_found}) # type: ignore
		self.mark_btn.toggle_disabled(False)

	def update_exists(self) -> None:
		# loop through file widgets and disable those that don't have files anymore, enable those that do
		# disable mark button if there are 0, enable if there are more
		for file_widget in self.file_widgets:
			if file_widget.file_path == None: continue
			file_widget.is_found = SETTINGS.default.accepted_file_extensions.get(Path(file_widget.file_path).suffix[1:], False)

			# file_widget.found = self.check_exists()

	def choose_config(self):
		file_path = fd.askopenfilename(initialdir="./", title="Select Automarker configuration file",filetypes=(("json files","*.json"),))
		file = ConfigFile(file_path)
		if file.valid:
			self.set_config_file(file)
		else:
			print(file.error)

	def set_config_file(self, file: ConfigFile):
		self._config_file = file
		self.current_config_text.config(text=file.short_path)
		for file_widget in self.file_widgets:
			file_widget.destroy()
		self.file_widgets.clear()
		found = self.populate_files_list(file)
		self.mark_btn.toggle_disabled(found == 0)

	def choose_file(self, file: str):
		"""
		Allow the user to choose the actual file for a given file name & save it if it is valid
		"""
		types = []
		for extension, accepted in SETTINGS.default.accepted_file_extensions.items():
			if accepted:
				types.append((f"{extension} files", f"*.{extension}"))
		file_path = fd.askopenfilename(initialdir="./", title="Select program file to mark", filetypes=types)
		p = Path(file_path)
		if p.exists() and p.is_file():
			SETTINGS.default.script_paths[file.lower()] = file_path
			self.mark_btn.toggle_disabled(False)
			return p.name
		return file

	def populate_files_list(self, file: ConfigFile) -> int:
		"""
		Add file widgets for all the files to be marked in the given config file and return the
		number of those files found
		"""
		total = 0
		for question in file.questions:
			path = SETTINGS.default.script_paths.get(question["name"].lower(), None)
			if path == None:
				path = self._config_file.directory
				found = self.check_exists(question["name"], path)
			elif os.path.exists(path):
				found = path
			else:
				del SETTINGS.default.script_paths[question["name"].lower()]
				found = ""
			self.file_widgets.append(
				FileWidget(
					self.files,
					question["name"],
					len(question["trials"]),
					command=self.choose_file,
					is_found=found != "",
					file_path=found if found else None
				)
			)
			self.file_widgets[-1].pack(anchor="n", padx=Window.padding, pady=Window.padding/2)
			if found != "":
				total += 1
		return total

	def check_exists(self, name: str, path: str) -> str:
		"""Return the complete path of the file if it exists, else an empty string"""
		try:
			files = {i.lower(): i for i in os.listdir(path)}
		except FileNotFoundError:
			return ""
		for ext, v in SETTINGS.default.accepted_file_extensions.items():
			if v and f"{name.lower()}.{ext}" in files:
				return f"{path}/{files[f'{name.lower()}.{ext}']}"
		return ""

	def files_found(self) -> int:
		total = 0
		for file_widget in self.file_widgets:
			total += file_widget.is_found
		return total