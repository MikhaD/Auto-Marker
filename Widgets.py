from tkinter import END, Frame, Label, Tk, Widget, Button as BTN, Event, Canvas
from tkinter.scrolledtext import ScrolledText as ST
from typing import Any, Callable, Literal, Optional, Union
from Settings import SETTINGS

class Heading(Label):
	def __init__(self, master: Union[Widget, Tk], text: str, level: Literal[1, 2, 3, 4]=1, code: bool=False,**kwargs: Any):
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

class Text(Label):
	def __init__(self, master: Union[Widget, Tk], text: str, bold: bool=False, **kwargs: Any):
		super().__init__(master,
			text=text,
			font=(SETTINGS.font.regular,
				SETTINGS.font.size.regular,
				"bold" if bold else "normal"),
			fg=SETTINGS.theme.fg_0,
			bg=SETTINGS.theme.bg_0,
			wraplength=500,
			**kwargs
		)

class Button(BTN):
	def __init__(self, master: Union[Widget, Tk], text: str, command: Callable, **kwargs: Any):
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

class ScrolledText(ST):
	def __init__(self, master: Union[Widget, Tk], **kwargs: Any):
		super().__init__(master,
			font=(SETTINGS.font.code,
				SETTINGS.font.size.code),
			bg=SETTINGS.theme.bg_1,
			fg=SETTINGS.theme.fg_1,
			borderwidth=0,
			highlightthickness=15,
			highlightbackground=SETTINGS.theme.bg_1,
			highlightcolor=SETTINGS.theme.bg_1,
			**kwargs
		)
		self.tag_configure("red", foreground=SETTINGS.theme.red)
		self.tag_configure("green", foreground=SETTINGS.theme.green)
		self.tag_configure("yellow", foreground=SETTINGS.theme.yellow)

	def print(self, text: str, tag: Optional[str]=None, end: str="\n"):
		if not tag:
			self.insert(END, text+end)
		else:
			self.insert(END, text+end, tag)

	def clear(self):
		self.delete("1.0", END)

class Details(Frame):
	_title: str
	def __init__(self, master: Union[Widget, Tk], title: str, body: Widget, level: Literal[1, 2, 3, 4] = 1, open: bool = True, width: int = 0, **kwargs: Any):
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

	def set_body(self, body: Widget):
		self.body = body
		self.body.config(bg=SETTINGS.theme.bg_0) # type: ignore
		if self.open: self.body.pack(anchor="n", fill="x")

	@property
	def title(self): return f"{'▼' if self.open else '►'} {self._title}"

	@title.setter
	def title(self, value: str): self._title = value

	def toggle(self, e: Event):
		self.open = not self.open
		self.summary.configure(text=self.title)
		if self.open:
			self.body.pack(anchor="n", fill="x")
		else:
			self.body.pack_forget()

class FileIcon(Canvas):
	OUTLINE = ((3, 3), (3, 28), (23, 28), (23, 11), (15, 3))
	def __init__(self, root: Union[Widget, Tk], is_found: bool, **kwargs: Any):
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

class FileWidget(Frame):
	def __init__(self, master: Widget | Tk, filename: str, trials: int, is_found: bool = False, **kwargs: Any):
		super().__init__(master,
			bg=SETTINGS.theme.bg_2,
			cursor="hand2",
			**kwargs
		)
		self.bind("<Button-1>", self.__action)

		self.icon = FileIcon(self, is_found, width=22, height=27, bg=SETTINGS.theme.bg_2)
		self.icon.pack(side="left", padx=5, pady=5)
		self.title = Heading(self, filename, 3, code=True, bg=SETTINGS.theme.bg_2, width=30, anchor="w", command=self.__action)
		self.title.pack(side="left", padx=10)
		self.filename = filename

		self._trials = [0, trials]
		self.passed_label = Heading(self, f"0/{trials}", 3, code=True, bg=SETTINGS.theme.bg_2, command=self.__action)
		self.passed_label.pack(side="left", padx=10)

	@property
	def trials(self) -> int:
		return self._trials[0]

	@trials.setter
	def trials(self, value: int):
		self._trials[0] = value
		self.passed_label.configure(text=f"{value}/{self._trials[1]}")

	def __action(self, e: Event):
		self.icon.found = not self.icon.found

class CheckBox(Frame):
	def __init__(self, master: Tk | Widget, text: str, value: str | int, checked: bool = False, command: Callable[[str | int, bool], None] | None = None, **kwargs: Any):
		super().__init__(master,
			bg=SETTINGS.theme.bg_0,
			cursor="hand2",
			**kwargs
		)
		self.value = value
		self.__command = command
		self.bind("<Button-1>", self.__action)

		self.box = Frame(self, width=20, height=20, bg=SETTINGS.theme.bg_3)
		self.box.pack(side="left", padx=5, pady=5)

		self.check = Frame(self.box, width=10, height=10, bg=SETTINGS.theme.fg_0)

		self.checked = checked

		self.title = Heading(self, text, 3, code=True, bg=SETTINGS.theme.bg_0, command=self.__action)
		self.title.pack(side="left", padx=5)

	def __action(self, e: Event):
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

class CheckBoxPanel(Frame):
	checkboxes: list[CheckBox]
	def __init__(self, master: Widget | Tk, labels: list[str], values: list[str | int], **kwargs: Any):
		assert len(labels) == len(values), "There should be the same number of values as there are labels"
		super().__init__(master, bg=SETTINGS.theme.bg_0, **kwargs)
		self.checkboxes = []
		for label, value in zip(labels, values):
			self.checkboxes.append(CheckBox(self, label, value, value in SETTINGS.default.accepted_file_extensions, command=self.on_checkbox_click))
			self.checkboxes[-1].pack(anchor="w", fill="x")

		self.pack(anchor="n", fill="x")

	def on_checkbox_click(self, value: str | int, checked: bool):
		SETTINGS.default.accepted_file_extensions[str(value)] = checked

	@property
	def values(self) -> list[str | int]:
		return [checkbox.value for checkbox in self.checkboxes if checkbox.checked]