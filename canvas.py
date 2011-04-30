from Tkinter import *

class Canvas:
	def __init__(self,parent):
		self.canvas = Canvas(parent, bg = 'gray20', relief=RAISED, highlightbackground="yellow")
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
		"""self.canvas.bind('<Button-1>',  self.onSelectElement)
		self.canvas.bind('<Button-3>',  self.onCreateElement)
		self.canvas.bind('<B1-Motion>',  self.onCameraMove)
		self.canvas.bind('<Motion>',  self.onMotion)"""

