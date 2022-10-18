import json
import subprocess
from os import path, listdir, remove, system
from sys import argv

DEFAULT_INPUT = "inputs.json"
TIMEOUT = 1
"""The default marking data file if no file is specified via the command line."""

def red(string: str): return f"[91m{string}[0m"
def green(string: str): return f"[92m{string}[0m"
def yellow(string: str): return f"[93m{string}[0m"
def bold(string: str): return f"[1m{string}[0m"

def fraction_string(value: int, max: int):
	"""
	Return the string `value`/`max` in green if `value == max`, yellow if `value >= max//2` or red
	if anything below.
	"""
	if value == max: return green(f"{value}/{max}")
	if value >= max//2: return yellow(f"{value}/{max}")
	return red(f"{value}/{max}")

class OutputError(ValueError):
	"""The output produced does not match."""
	pass

def compile(file: str):
	"""Attempt to compile the given java file. Return True if successful."""
	try:
		subprocess.check_output(["javac", file], stderr=subprocess.STDOUT)
		return True
	except subprocess.CalledProcessError as e:
		print(red(f"Failed to compile {file}"))
		print(e.output.decode().replace("^", red("^")))
	return False

if __name__ == "__main__":
	# Initialize terminal so colors work if using git bash
	system("tput init")
	f = open(argv[1] if len(argv) > 1 else DEFAULT_INPUT, "r")
	data = json.load(f)
	f.close()

	for file, question in enumerate(data["questions"], 1):
		print(bold(f"{f' Question {file} ':#^31}"))

		name = f"{question['name']}.java"
		valid = True
		passed = 0
		if (not path.exists(name)):
			print(red(f"Could not find {name}"))
			valid = False
		if valid:
				valid = compile(name)
		if valid:
			for j, trial in enumerate(question["trials"], 1):
				print(f"Trial {j:>2}: ", end="")
				try:
					out = subprocess.check_output(["java", question["name"]], input="\n".join(trial["input"]).encode(), stderr=subprocess.STDOUT, timeout=TIMEOUT)
					if out.decode().strip() == "\n".join(trial["output"]):
						print(green("Output correct"))
						passed += 1
					else: raise OutputError()
				except Exception as e:
					print(red("Output incorrect"))
					if type(e) is subprocess.TimeoutExpired:
						print(red(f"Killed after {TIMEOUT} second{'s' if TIMEOUT != 1 else ''}\n"))
					else:
						print("The expected output:")
						print("\n".join(trial["output"]))
						print("Your program produced:")
						if type(e) is OutputError:
							print(out.decode().strip(), end="\n\n")
						elif type(e) is subprocess.CalledProcessError:
							print(e.output.decode())
						else:
							print(e)

		print(f"{fraction_string(passed, len(question['trials']))} trials passed.\n")
		for file in listdir():
			if file.endswith(".class"):
				remove(file)