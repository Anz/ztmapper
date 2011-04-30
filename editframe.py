from Tkinter import *
from editor import *
from element import *

class EditButton:
	def __init__(self, parent, number, text, command, submenu):
		self.parent = parent
		self.number = number
		self.submenu = submenu

		self.frame = Frame(parent)
		self.frame.pack(fill=X)
		self.frame.bind('<Enter>', self.onEnter)
		self.frame.bind('<Leave>', self.onLeave)

		self.button = Button(self.frame, text=text, padx=15,activebackground="grey", fg="grey", bg="grey20", highlightthickness=0, relief=FLAT, anchor=W, command=command)
		self.button.pack(side=LEFT,fill=X,expand=1)

		self.canvas = Canvas(self.frame, highlightthickness=0, relief=FLAT, bd=0, bg="grey20", width=7, height=27)
		self.canvas.create_polygon((0, 10, 0, 16, 3, 13), fill="grey")
		if submenu != None:
			self.canvas.pack(side=RIGHT)

	def onEnter(self,event):
		self.button.config(fg="grey20", bg="grey")
		self.canvas.config(bg="grey")
		self.canvas.create_polygon((0, 10, 0, 16, 3, 13), fill="grey20")

		if self.submenu != None:
			x = int(self.parent.geometry().split("+")[1]) + int(self.parent.geometry().split("x")[0])
			y = int(self.parent.geometry().split("+")[2]) + self.number * 27
			self.submenu.show(Vec2(x,y))
			self.parent.deiconify()

	def onLeave(self,event):
		self.button.config(fg="grey", bg="grey20")
		self.canvas.config(bg="grey20")
		self.canvas.create_polygon((0, 10, 0, 16, 3, 13), fill="grey")

		if self.submenu != None:
			self.submenu.unshow()

class EditMenu:
	def __init__(self):
		self.root = Toplevel(bg='grey20')
		self.root.overrideredirect(1)
		self.root.withdraw()
		self.items = 0
		
	def additem(self, text, command, submenu):
		EditButton(self.root, self.items, text, command, submenu)
		self.items += 1

	def show(self, position):
		self.root.geometry("%dx%d%+d%+d" % (116, self.items * 27, position.x, position.y))
		self.root.deiconify()

	def unshow(self):
		self.root.withdraw()

class EditFrame:
	def __init__(self, editor, space):
		self.editor = editor
		self.space = space
		self.addsubmenu = EditMenu()
		self.addsubmenu.additem("Box", None, None)
		self.addsubmenu.additem("Zombie", None, None)
		self.addsubmenu.additem("Bat", None, None)
		self.addsubmenu.additem("Cave", None, None)

		self.layersubmenu = EditMenu()
		self.layersubmenu.additem("On Top", None, None)
		self.layersubmenu.additem("On Botton", None, None)
		self.layersubmenu.additem("Upper", None, None)
		self.layersubmenu.additem("Lower", None, None)

		self.main = EditMenu()
		self.main.additem("Add", self.addElement, self.addsubmenu)
		self.main.additem("Layer", None, self.layersubmenu)
		self.main.additem("Move", None, None)
		self.main.additem("Delete", self.deleteSelectedElements, None)
		self.main.additem("Properties", None, None)

	def show(self, absolute, relative):
		self.mouse = relative
		self.main.show(absolute)

	def unshow(self):
		self.main.unshow()

	def addElement(self):
		position = self.editor.getScreenInSpace(self.mouse)
		element = Element("box", position, 0.0, 0.0)
		self.space.addElement(element)
		self.editor.render(self.space)

	def deleteSelectedElements(self):
		self.main.unshow()
		self.space.deleteSelection()
		self.editor.render(self.space)
