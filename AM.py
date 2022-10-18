
from tkinter import Frame, Label, ttk

from Settings import SETTINGS
from Widgets import Button, FileWidget, Heading, ScrolledText
from Panels import Config, Window
#   _    _ _           _                 _____      _
#  | |  | (_)         | |               /  ___|    | |
#  | |  | |_ _ __   __| | _____      __ \ `--.  ___| |_ _   _ _ __
#  | |/\| | | "_ \ / _` |/ _ \ \ /\ / /  `--. \/ _ \ __| | | | "_ \
#  \  /\  / | | | | (_| | (_) \ V  V /  /\__/ /  __/ |_| |_| | |_) |
#   \/  \/|_|_| |_|\__,_|\___/ \_/\_/   \____/ \___|\__|\__,_| .__/
#                                                            | |
#                                                            |_|

labels: dict[str, Label] = {}
buttons: dict[str, Button] = {}

ttk.Style
root = Window("Mikha's Auto Marker")
root.configure(bg=SETTINGS.theme.bg_0)

options = Frame(root, bg=SETTINGS.theme.bg_0, width=200)
options.pack(side="left", fill="both", expand=True)

labels["am"] = Heading(options, text="AUTOMATIC MARKER")
labels["am"].pack(anchor="n", pady=Window.padding)

config = Config(options)
config.pack(anchor="n", pady=Window.padding)

FileWidget(options, "Palindrome", 7).pack(anchor="n", pady=Window.padding)
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