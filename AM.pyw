
from tkinter import Frame

from Settings import SETTINGS
from Widgets import ScrolledText
from Panels import ControlsFrame, Window
#   _    _ _           _                 _____      _
#  | |  | (_)         | |               /  ___|    | |
#  | |  | |_ _ __   __| | _____      __ \ `--.  ___| |_ _   _ _ __
#  | |/\| | | "_ \ / _` |/ _ \ \ /\ / /  `--. \/ _ \ __| | | | "_ \
#  \  /\  / | | | | (_| | (_) \ V  V /  /\__/ /  __/ |_| |_| | |_) |
#   \/  \/|_|_| |_|\__,_|\___/ \_/\_/   \____/ \___|\__|\__,_| .__/
#                                                            | |
#                                                            |_|

root = Window("Mikha's Auto Marker")

controls = ControlsFrame(root)


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