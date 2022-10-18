import json
from sys import argv

questions = tuple(i for i in input("List the questions you wish to scrape the data for (space separated):\n").split(" "))

with open(argv[1], "r") as f:
	line = next(f)
	while ("Question" not in line or line.strip().split(" ")[1] not in questions): line = next(f)
	question = {"trials": []}
	trial_no = 1
	while "Score for question" not in line:
		if f"Trial {trial_no}" in line:
			trial_no += 1
			trial = {"input": [], "output": []}
			while "The expected output was:" not in line: line = next(f)
			line = next(f)
			while line != "\n":
				trial["output"].append(line.strip())
				line = next(f)
			while line != "Input supplied to your program:\n": line = next(f)
			line = next(f)
			while line != "\n":
				trial["input"].append(line.strip())
				line = next(f)
			question["trials"].append(trial)
		else:
			line = next(f)

with open("qs.json", "w") as f:
	json.dump(question, f, indent="\t")