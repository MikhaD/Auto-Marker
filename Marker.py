from pathlib import Path
import subprocess
import tempfile
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import Any
from ConfigFile import ConfigFile
from Settings import SETTINGS

class OutputError(ValueError):
	"""The output produced does not match."""
	pass

class Marker(ScrolledText):
	def __init__(self, master: tk.Widget|tk.Tk, **kwargs: Any):
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
		self.tag_configure("bold", font=(SETTINGS.font.code, SETTINGS.font.size.code, "bold"))
		self.tag_configure("large", font=(SETTINGS.font.code, int(SETTINGS.font.size.code*1.5)))
		self.tag_configure("bold-large", font=(SETTINGS.font.code, int(SETTINGS.font.size.code*1.5), "bold"))

	def print(self, text: str="", *tags: str, end: str="\n"):
			self.insert(tk.END, text+end, tags)

	def clear(self):
		self.delete("1.0", tk.END)

	def mark(self, config: ConfigFile, paths: dict[str, str]):
		self.clear()

		for file, question in enumerate(config.questions, 1):
			self.print(f"{f' Question {file} ':#^31}", "bold-large")
			if question["name"].lower() not in paths:
				self.print(f"Could not find {question['name']}", "red")
				continue

			passed = 0
			path = Path(paths[question["name"].lower()])
			if path.suffix == ".java":
				with tempfile.TemporaryDirectory(prefix="automarker-") as tempdir:
					try:
						subprocess.check_output(["javac", "-d", tempdir, "-cp", tempdir, path.as_posix()])
					except subprocess.CalledProcessError as e:
						self.print(f"Failed to compile {path.name}", "red")
						self.print(e.output.decode())
						continue
					for i, trial in enumerate(question["trials"], 1):
						self.print(f"Trial {i:>2}: ", end="")
						out = b""
						try:
							out =subprocess.check_output(["java", "-cp", tempdir, path.stem], input="\n".join(trial["input"]).encode(), stderr=subprocess.STDOUT, timeout=SETTINGS.default.timeout)
							if out.decode().strip() == "\n".join(trial["output"]):
								self.print("Output correct", "green")
								passed += 1
							else: raise OutputError()
						except Exception as e:
							self.print("Output incorrect", "red")
							if type(e) is subprocess.TimeoutExpired:
								self.print(f"Killed after {SETTINGS.default.timeout} second{'s' if SETTINGS.default.timeout != 1 else ''}\n", "red")
							else:
								self.print("The expected output:")
								self.print("\n".join(trial["output"]))
								self.print("\nYour program produced:")
								if type(e) is OutputError:
									self.print(out.decode().strip(), end="\n\n")
								elif type(e) is subprocess.CalledProcessError:
									self.print(e.output.decode())
								else:
									self.print(str(e))

						# self.print(f"{fraction_string(passed, len(question['trials']))} trials passed.\n")
			elif path.suffix == ".py":
				pass
			else:
				self.print(f"Unknown file type {path.suffix}", "red")