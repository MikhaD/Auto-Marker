
from tkinter import Frame
from sys import argv

from Settings import SETTINGS
from Widgets import ScrolledText
from Panels import ControlsFrame, Window
from ConfigFile import ConfigFile


root = Window("Mikha's Auto Marker")
conf = None
if (len(argv) > 1):
	conf = ConfigFile(argv[1])
	print(1, conf.error)
if not conf or not conf.valid:
	conf = ConfigFile(SETTINGS.default.config_file)
	print(2, conf.error)
if conf and not conf.valid:
	conf = None
	print(3, conf)
controls = ControlsFrame(root, conf)


# FileWidget(options, "Palindrome", 7).pack(anchor="n", padx=Window.padding, pady=Window.padding/2)
# FileWidget(options, "Cycling", 7).pack(anchor="n", padx=Window.padding, pady=Window.padding/2)
# FileWidget(options, "Prime", 7).pack(anchor="n", padx=Window.padding, pady=Window.padding/2)
# In order for the window to resize correctly, both output and options need to be frames
out_frame = Frame(root, bg=SETTINGS.theme.bg_0, width=300)
out_frame.pack(side="right", fill="both", expand=True)
output = ScrolledText(out_frame)
output.pack(padx=Window.padding, pady=Window.padding, fill="both", expand=True)
output.print("Hello World", "green")
output.print("Hello World", "yellow")
output.print("Hello World", "red", end="")
output.print("Hello World")

root.mainloop()