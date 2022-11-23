import tkinter as tk
from typing import Any, Callable, Literal
from Settings import SETTINGS

class Heading(tk.Label):
	def __init__(self, master: tk.Widget|tk.Tk, text: str, level: Literal[1, 2, 3, 4]=1, code: bool=False,**kwargs: Any):
		command = kwargs.pop("command", None)
		if   level == 2: font_size = SETTINGS.font.size.h2
		elif level == 3: font_size = SETTINGS.font.size.h3
		elif level == 4: font_size = SETTINGS.font.size.regular
		else:            font_size = SETTINGS.font.size.h1
		super().__init__(master,
			text=text,
			fg=SETTINGS.theme.fg_0,
			bg=kwargs.pop("bg", SETTINGS.theme.bg_0),
			font=(SETTINGS.font.code if code else SETTINGS.font.regular, font_size, "bold"),
			**kwargs
		)
		if command: self.bind("<Button-1>", command)

class Text(tk.Label):
	def __init__(self, master: tk.Widget|tk.Tk, text: str, bold: bool=False, code: bool=False, bg: str|None=None, fg: str|None=None, **kwargs: Any):
		super().__init__(master,
			text=text,
			font=(SETTINGS.font.code if code else SETTINGS.font.regular,
				SETTINGS.font.size.regular,
				"bold" if bold else "normal"),
			fg= fg if fg else SETTINGS.theme.fg_0,
			bg= bg if bg else SETTINGS.theme.bg_0,
			wraplength=500,
			**kwargs
		)

class Button(tk.Button):
	disabled: bool
	def __init__(self, master: tk.Widget|tk.Tk, text: str, command: Callable, disabled: bool = False, **kwargs: Any):
		super().__init__(master,
			text=text,
			font=(SETTINGS.font.regular,
				SETTINGS.font.size.button, "bold"),
			fg=SETTINGS.theme.fg_0,
			bg=SETTINGS.theme.accent_0,
			activebackground=SETTINGS.theme.accent_1,
			activeforeground=SETTINGS.theme.fg_0,
			width=20,
			pady=5,
			border=0,
			cursor="hand2",
			command=command,
			**kwargs
		)
		self.toggle_disabled(disabled)

	def toggle_disabled(self, state: bool | None = None):
		if state == None:
			state = not self.disabled
		self.disabled = state
		if self.disabled:
			self["state"] = "disabled"
			self.config(cursor="none")
			self.config(bg=SETTINGS.theme.bg_disabled)
			self.config(fg=SETTINGS.theme.fg_disabled)
			self.config(cursor="")
		else:
			self["state"] = "active"
			self.config(cursor="hand2")
			self.config(bg=SETTINGS.theme.accent_1)
			self.config(fg=SETTINGS.theme.fg_0)

class Details(tk.Frame):
	_title: str
	def __init__(self, master: tk.Widget|tk.Tk, title: str, level: Literal[1, 2, 3, 4] = 1, open: bool = True, width: int = 0, **kwargs: Any):
		self.open = open
		self.title = title
		super().__init__(master,
			bg=SETTINGS.theme.bg_0,
			**kwargs
		)
		self.summary = Heading(self, self.title, level, cursor="hand2", command=self.toggle)
		if width:
			self.summary.configure(width=width)
		self.summary.pack(anchor="n")

	def set_body(self, body: tk.Widget):
		self.body = body
		self.body.config(bg=SETTINGS.theme.bg_0) # type: ignore
		if self.open: self.body.pack(anchor="n", fill="x")

	@property
	def title(self): return f"{'▼' if self.open else '►'} {self._title}"

	@title.setter
	def title(self, value: str): self._title = value

	def toggle(self, e: tk.Event):
		self.open = not self.open
		self.summary.configure(text=self.title)
		if self.open:
			self.body.pack(anchor="n", fill="x")
		else:
			self.body.pack_forget()

class FileIcon(tk.Canvas):
	OUTLINE = ((3, 3), (3, 28), (23, 28), (23, 11), (15, 3))
	def __init__(self, root: tk.Widget|tk.Tk, is_found: bool, **kwargs: Any):
		super().__init__(root, highlightthickness=0, **kwargs)
		self.found = is_found

	@property
	def found(self) -> bool:
		return self._found

	@found.setter
	def found(self, value: bool):
		self._found = value
		self.delete("all")
		if value:
			self.draw_found()
		else:
			self.draw_not_found()

	def draw_found(self):
		self.create_polygon(*FileIcon.OUTLINE, fill=SETTINGS.theme.green, width=0)
		self.create_line((6, 15), (11, 21), width=4, fill=SETTINGS.theme.bg_2)
		self.create_line((10, 20), (18, 11), width=4, fill=SETTINGS.theme.bg_2)

	def draw_not_found(self):
		self.create_polygon(*FileIcon.OUTLINE, fill=SETTINGS.theme.red, width=0)
		self.create_line((8, 12), (18, 22), width=4, fill=SETTINGS.theme.bg_2)
		self.create_line((18, 12), (8, 22), width=4, fill=SETTINGS.theme.bg_2)

class FileWidget(tk.Frame):
	def __init__(self, master: tk.Widget|tk.Tk, name: str, trials: int, command: Callable, is_found: bool=False, file_path: str|None = None, **kwargs: Any):
		super().__init__(
			master,
			bg=SETTINGS.theme.bg_2,
			cursor="hand2",
			**kwargs
		)
		self.bind("<Button-1>", self.__action)

		self.command = command
		self.icon = FileIcon(self, is_found, width=22, height=27, bg=SETTINGS.theme.bg_2)
		self.icon.pack(side="left", padx=5, pady=5)
		self.title = Heading(self, name, 3, code=True, bg=SETTINGS.theme.bg_2, width=30, anchor="w", command=self.__action)
		self.title.pack(side="left", padx=10)
		self.name = name
		self.file_path = file_path
		# if self.filename:
		# 	self.tooltip = tix.Balloon(master)  # type: ignore
		# 	self.tooltip.bind_widget(self, balloonmsg=self.filename)

		self._trials = [0, trials]
		self.passed_label = Heading(self, f"0/{trials}", 3, code=True, bg=SETTINGS.theme.bg_2, command=self.__action)
		self.passed_label.pack(side="left", padx=10)

	def __action(self, event: tk.Event | None = None):
		self.file_path = self.command(self.name)
		self.is_found = self.file_path != None

		# print(self.tooltip.keys())
		# self.tooltip.message.config(text=self.filename)

	@property
	def trials(self) -> int:
		return self._trials[0]

	@property
	def is_found(self) -> bool:
		return self.icon.found

	@is_found.setter
	def is_found(self, value: bool):
		self.icon.found = value

	@trials.setter
	def trials(self, value: int):
		self._trials[0] = value
		self.passed_label.configure(text=f"{value}/{self._trials[1]}")

class CheckBox(tk.Frame):
	def __init__(self, master: tk.Tk|tk.Widget, text: str, value: str | int, checked: bool = False, command: Callable[[str | int, bool], None] | None = None, **kwargs: Any):
		super().__init__(master,
			bg=SETTINGS.theme.bg_0,
			cursor="hand2",
			width=500,
			height=35,
			**kwargs
		)
		self.pack_propagate(False)
		self.value = value
		self.__command = command
		self.bind("<Button-1>", self.__action)

		self.box = tk.Frame(self, width=20, height=20, bg=SETTINGS.theme.bg_3)
		self.box.pack(side="left", padx=5, pady=5)

		self.check = tk.Frame(self.box, width=10, height=10, bg=SETTINGS.theme.fg_0)

		self.checked = checked

		self.title = Heading(self, text, 3, code=True, bg=SETTINGS.theme.bg_0, command=self.__action)
		self.title.pack(side="left", padx=5)

	def __action(self, e: tk.Event):
		self.checked = not self.checked
		if self.__command: self.__command(self.value, self.checked)

	@property
	def checked(self) -> bool:
		return self.__checked

	@checked.setter
	def checked(self, value: bool):
		self.__checked = value
		if self.__checked:
			self.check.pack(padx=5, pady=5)
		else:
			self.check.pack_forget()

class CheckBoxPanel(tk.Frame):
	checkboxes: list[CheckBox]
	command: Callable
	def __init__(self, master: tk.Widget|tk.Tk, labels: list[str], values: list[str | int], command: Callable, **kwargs: Any):
		assert len(labels) == len(values), "There should be the same number of values as there are labels"
		super().__init__(master, bg=SETTINGS.theme.bg_0, **kwargs)
		self.checkboxes = []
		self.command = command
		for label, value in zip(labels, values):
			self.checkboxes.append(CheckBox(self, label, value, SETTINGS.default.accepted_file_extensions.get(SETTINGS.FILE_TYPES[label], False), command=self.on_checkbox_click))
			self.checkboxes[-1].pack(anchor="n")

		self.pack(anchor="n")

	def on_checkbox_click(self, value: str | int, checked: bool):
		SETTINGS.default.accepted_file_extensions[str(value)] = checked
		self.command()

	@property
	def values(self) -> list[str | int]:
		return [checkbox.value for checkbox in self.checkboxes if checkbox.checked]