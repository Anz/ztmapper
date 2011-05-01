from Tkinter import *
from editor import *
from element import *
from util import *

class EditButton:
	def __init__(self, parent, text, command):
		self.parent = parent
		self.command = command
		self.text = text

		self.frame = Frame(parent.root)
		self.frame.pack(fill=X)
		self.frame.bind('<Enter>', self.onEnter)

		self.button = Button(
			self.frame, 
			text=text, 
			padx=15,
			disabledforeground="black",
			activebackground="grey", 
			fg="grey", 
			bg="grey20", 
			highlightthickness=0, 
			relief=FLAT, 
			anchor=W, 
			command=self.onClick)
		self.button.pack(side=LEFT,fill=X,expand=1)

	def onEnter(self,event):
		if self.parent.submenu != None:
			self.parent.submenu.unshow()
			self.parent.submenu = None

	def onClick(self):
		editmenu = self.parent
		while editmenu != None:
			editmenu.unshow()
			editmenu = editmenu.parent

		if self.command != None:
			self.command(self.text)

class EditSubButton:
	def __init__(self, parent, number, text, submenu):
		self.parent = parent
		self.number = number
		self.submenu = submenu
		self.text = text

		self.frame = Frame(parent.root)
		self.frame.pack(fill=X)
		self.frame.bind('<Enter>', self.onEnter)
		self.frame.bind('<Leave>', self.onLeave)

		self.button = Button(self.frame, text=text, padx=15,activebackground="grey", fg="grey", bg="grey20", highlightthickness=0, relief=FLAT, anchor=W)
		self.button.pack(side=LEFT,fill=X,expand=1)

		self.canvas = Canvas(self.frame, highlightthickness=0, relief=FLAT, bd=0, bg="grey20", width=7, height=27)
		self.canvas.create_polygon((0, 10, 0, 16, 3, 13), fill="grey")
		self.canvas.pack(side=RIGHT)

	def onEnter(self,event):
		if self.parent.submenu != None:
			self.parent.submenu.unshow()
			self.parent.submenu = None

		self.button.config(fg="grey20", bg="grey")
		self.canvas.config(bg="grey")
		self.canvas.create_polygon((0, 10, 0, 16, 3, 13), fill="grey20")


		self.parent.submenu = self.submenu
		x = int(self.parent.root.geometry().split("+")[1]) + int(self.parent.root.geometry().split("x")[0])
		y = int(self.parent.root.geometry().split("+")[2]) + self.number * 27
		self.submenu.show(Vec2(x,y))
		self.parent.root.deiconify()

	def onLeave(self,event):
		self.button.config(fg="grey", bg="grey20")
		self.canvas.config(bg="grey20")
		self.canvas.create_polygon((0, 10, 0, 16, 3, 13), fill="grey")

class EditMenu:
	def __init__(self):
		self.parent = None
		self.root = Toplevel(bg='grey20')
		self.root.overrideredirect(1)
		self.root.withdraw()
		self.buttons = []
		self.submenu = None
		
	def additem(self, text, command):
		self.buttons.append(EditButton(self, text, command))

	def addsubmenu(self, text, submenu):
		submenu.parent = self
		self.buttons.append(EditSubButton(self, len(self.buttons), text, submenu))


	def show(self, position):
		self.root.geometry("%dx%d%+d%+d" % (116, len(self.buttons) * 27, position.x, position.y))
		self.root.deiconify()

	def unshow(self):
		if self.submenu != None:
			self.submenu.unshow()
		self.root.withdraw()

class EditFrame:
	def __init__(self, editor, space, images):
		self.editor = editor
		self.space = space
		self.addsubmenu = EditMenu()
		for image in images:
			self.addsubmenu.additem(image, self.addElement)

		self.layersubmenu = EditMenu()
		self.layersubmenu.additem("On Top", None)
		self.layersubmenu.additem("On Botton", None)
		self.layersubmenu.additem("Upper", None)
		self.layersubmenu.additem("Lower", None)

		self.main = EditMenu()
		self.main.addsubmenu("Add", self.addsubmenu)
		self.main.addsubmenu("Layer", self.layersubmenu)
		self.main.additem("Move", self.moveSelection)
		self.main.additem("Unselect all", self.unselectElements)
		self.main.additem("Delete", self.deleteSelectedElements)
		self.main.additem("Properties", None)

	def show(self, absolute, relative):
		self.mouse = relative
		self.main.show(absolute)

	def unshow(self):
		self.main.unshow()

	def addElement(self,label):
		position = self.editor.getScreenInSpace(self.mouse)
		element = Element(label, position, 0.0, 0.0)
		self.space.addElement(element)
		self.editor.render(self.space)

	def deleteSelectedElements(self,label):
		self.space.deleteSelection()
		self.editor.render(self.space)

	def moveSelection(self,label):
		self.space.mode = 1

	def unselectElements(self,label):
		self.space.selection = []
