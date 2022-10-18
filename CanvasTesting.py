from tkinter import Tk, Canvas
from typing import Any



class FileIcon(Canvas):
	OUTLINE = ((3, 3), (3, 28), (23, 28), (23, 11), (15, 3))
	def __init__(self, root: Tk, found: bool, **kwargs: Any):
		super().__init__(root, **kwargs)
		self.found = found

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
		self.create_polygon(*FileIcon.OUTLINE, fill="#40B140", width=0)
		self.create_line((6, 15), (11, 21), width=4, fill="black")
		self.create_line((10, 20), (18, 11), width=4, fill="black")

	def draw_not_found(self):
		self.create_polygon(*FileIcon.OUTLINE, fill="#FE2D2D", width=0)
		self.create_line((8, 12), (18, 22), width=4, fill="black")
		self.create_line((18, 12), (8, 22), width=4, fill="black")


root = Tk()
root.geometry("800x600")
root.title("Canvas Demo - Polygon")

canvas = FileIcon(root, True, width=22, height=27, bg="#31353B")
canvas.pack()
root.mainloop()