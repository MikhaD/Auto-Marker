
from tkinter import Frame
from sys import argv

from Settings import SETTINGS
from Marker import Marker
from Panels import ControlsFrame, Window
from ConfigFile import ConfigFile


root = Window("Mikha's Auto Marker")
# In order for the window to resize correctly, both output and options need to be frames
out_frame = Frame(root, bg=SETTINGS.theme.bg_0, width=300)
out_frame.pack(side="right", fill="both", expand=True)
output = Marker(out_frame)

conf = None
if (len(argv) > 1):
	conf = ConfigFile(argv[1])
if not conf or not conf.valid:
	conf = ConfigFile(SETTINGS.default.config_file)
if conf and not conf.valid:
	conf = None
controls = ControlsFrame(root, conf, output)

output.pack(padx=Window.padding, pady=Window.padding, fill="both", expand=True)

root.mainloop()