# Auto Marker
This is a tool to automatically validate the correctness of your code by passing it input via the command line and comparing the output to the expected output. It is designed to be similar to the Automarker available to Computer Science students at the University of Cape Town via Vula.
## Inspiration
I was inspired to make this to help a friend practice on a set of questions she did not have access to Vula's Automarker for. Its original purpose was for testing code for other people's tests or past tests where UCTs Automarker is not available.
However, it has proved to be useful for testing code before submitting it to UCTs Automarker as well, as it is much faster to run and does not require the files to be zipped and uploaded.
## Design Decisions
The driving factor behind the design is the desire for the entire codebase to be in one file without dependencies to make it as easy as possible to distribute and use.
## Usage
In order to use this automatic marker you will need python 3 and a file containing the inputs and expected outputs for a set of questions in JSON format. The schema for these files is as follows:
```json
{
	"questions": [
		{
			"name": "code file name",
			"input": [
				"input line 1",
				"input line 2",
			],
			"output": [
				"output line 1",
				"output line 2",
			]
		},
		{
			"name": "BinarySearch",
			"input": [
				"5",
				"1 2 3 4 5",
				"3"
			],
			"output": [
				"2"
			]
		}
	]
}
```
At the moment it only works with Java code, but I plan to add support for python in the near future.