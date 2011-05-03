from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from traceback import *
from element import *
from space import *
from image import *
from editor import *
from level import *
from editframe import *
from util import *
from io import *
from subprocess import *
		
class Application:

	def __init__(self):
		self.space = Space()	
		self.selector = 0
		self.clipboard = []
		self.multiselection = 0

		self.lastx = 0
		self.lasty = 0

		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.onWindowClose)
		self.root.report_callback_exception = self.catch_exception
		self.root.report_callback_exception = self.catch_exception
		self.root.title("ZTG Map Editor (ztmapper)")
		self.root.bind_all('<Expose>', self.onRedraw)
		self.root.bind_all('w', self.onUp)
		self.root.bind_all('a', self.onLeft)
		self.root.bind_all('s', self.onDown)
		self.root.bind_all('d', self.onRight)
		self.root.bind_all('<Delete>', self.onDelete)
		self.root.bind_all('<Control-a>', self.onSelectAll)
		self.root.bind_all('<Shift-Tab>', self.onBackElement)
		self.root.bind_all('<Tab>', self.onNextElement)
		self.root.bind_all('<Control_L>', self.onMultiSelectionEnable)
		self.root.bind_all('<KeyRelease-Control_L>', self.onMultiSelectionDisable)
		self.root.bind_all('<Control-o>', self.onShortOpen)
		self.root.bind_all('<Control-s>', self.onShortSave)
		self.root.bind_all('<Control-c>', self.onCopy)
		self.root.bind_all('<Control-v>', self.onPaste)

		self.images = loadImages()

		menubar = Menu(self.root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open", command=self.onOpen)
		filemenu.add_command(label="Save", command=self.onSave)
		filemenu.add_command(label="Save As", command=self.onSaveAs)
		filemenu.add_command(label="Close", command=self.onClose)
		menubar.add_cascade(label="File", menu=filemenu)
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Reset Camera", command=self.onCameraReset)
		editmenu.add_command(label="Test Map", command=self.onStartGame)
		menubar.add_cascade(label="Edit", menu=editmenu)
		self.root.config(menu=menubar)

		statusbar = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W)
		statusbar.pack(side=BOTTOM, fill=X)
		self.camstatus = Label(statusbar, text="", bd=1, relief=GROOVE, anchor=W)
		self.camstatus.grid(row=0, column=0)
		self.mousestatus = Label(statusbar, text="", bd=1, relief=GROOVE, anchor=W)
		self.mousestatus.grid(row=0, column=1)

		self.canvas = Canvas(self.root, bg = 'gray20', relief=RAISED, highlightbackground="yellow")
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
		self.canvas.bind('<Button-1>',  self.onSelect)
		self.canvas.bind('<Button-3>',  self.onEdit)
		self.canvas.bind('<B1-Motion>',  self.onMove)
		self.canvas.bind('<Motion>',  self.onMotion)

		self.editor = Editor(self.canvas, self.images)
		self.editframe = EditFrame(self.editor, self.space, self.images)

		self.root.update_idletasks()
		self.root.geometry("%sx%s+0+0" % self.root.maxsize())
		self.update()
		self.root.mainloop()
		
	def update(self):
		self.editor.render(self.space)

	def onEdit(self, event):
		self.editframe.show(Vec2(event.x_root, event.y_root), Vec2(event.x, event.y))
		
	def onSelect(self, event):
		self.editframe.unshow()
		self.space.mode = 0

		self.lastx = event.x
		self.lasty = event.y
		i = 0
		matches = []

		for element in self.space.elements:
			image = self.images[element.type]
			size = Vec2(image.width(), image.height()) / Vec2(2,2)
			min = element.pos - size
			max = element.pos + size
			mouse = self.editor.getScreenInSpace(Vec2(event.x, event.y))
			if min < mouse and mouse < max:
				matches.append(i)
			i += 1

		if len(matches) == 0:
			return
		if self.multiselection == 0:
			self.space.selection = [ matches[self.selector % len(matches)] ]
		else:
			for selected in matches:
				if selected in self.space.selection:
					self.space.selection.remove(selected)
				else:
					self.space.selection.append(selected)
			
		self.update()
		self.selector += 1
	
	def onMove(self,event):
		diff = Vec2(event.x - self.lastx, self.lasty - event.y)
		if self.space.mode == 0:
			self.editor.camera -= diff
		self.update()
		self.lastx = event.x
		self.lasty = event.y

	def onMotion(self,event):
		diff = Vec2(event.x - self.lastx, self.lasty - event.y)
		if self.space.mode == 1:
			self.space.moveSelection(diff)
			self.space.saved = 0
		self.lastx = event.x
		self.lasty = event.y
		self.update()

	def onCameraReset(self):
		self.editor.camera = Vec2(0,0)
		self.update()
	
	def onStartGame(self):
		Popen("/home/anz/workspace/ztg/img /home/anz/ztmapper/cave.map", shell=True, executable="/home/anz/workspace/ztg/bin/ztg")

	def onLeft(self, event):
		if len(self.space.selection) != 0:
			self.space.saved = 0
		self.space.moveSelection(Vec2(-1,0))
		self.update()
	
	def onRight(self, event):
		if len(self.space.selection) != 0:
			self.space.saved = 0
		self.space.moveSelection(Vec2(1,0))
		self.update()

	def onUp(self, event):
		if len(self.space.selection) != 0:
			self.space.saved = 0
		self.space.moveSelection(Vec2(0,1))
		self.update()

	def onDown(self, event):
		if len(self.space.selection) != 0:
			self.space.saved = 0
		self.space.moveSelection(Vec2(0,-1))
		self.update()

	def onDelete(self, event):
		if len(self.space.selection) != 0:
			self.space.saved = 0
		self.space.deleteSelection()
		self.update()
	
	def onBackElement(self,event):
		self.space.previous()
		selecteds = self.space.getSelected()
		if len(selecteds) == 1:
			self.editor.camera = selecteds[0].pos
		self.update()
	
	def onNextElement(self,event):
		self.space.next()
		selecteds = self.space.getSelected()
		if len(selecteds) == 1:
			self.editor.camera = selecteds[0].pos
		self.update()
		
	def onSelectAll(self,event):
		self.space.selection = range(len(self.space.elements))
		self.update()
		
	def onCopy(self,event):
		self.clipboard = []
		selecteds = self.space.getSelected()
		for selected in selecteds:
			element = element_copy(selected)
			element.pos -= self.editor.camera
			self.clipboard.append(element)
		
	def onPaste(self,event):
		self.space.selection = []
		for copy in self.clipboard:
			element = element_copy(copy)
			element.pos += self.editor.camera
			self.space.selection.append(len(self.space.elements))
			self.space.elements.append(element)
			self.space.saved = 0
		self.update()
		
	def onMultiSelectionEnable(self,event):
		self.multiselection = 1

	def onMultiSelectionDisable(self,event):
		self.multiselection = 0
		
	def onOpen(self):
		self.path = askopenfilename(filetypes = [('ZTG Map File', '*.map')])
		if self.path == None or self.path == "":
			return
		file = open(self.path, "r")
		mapRead(file, self.space.elements, self.images)
		file.close()
		curelement = 0
		element = self.space.elements[curelement]
		self.editor.camera = Vec2(0,0)
		self.space.saved = 1
		self.update()

	def onShortOpen(self,event):
		self.onOpen()

	def onSave(self):
		if self.path != None and self.path != "":
			file = open(self.path, "w")
			mapWrite(self.space.elements, file)
			file.close()
			self.saved = 1
			
	def onShortSave(self,event):
		self.onSave()

	def onSaveAs(self):
		self.path = asksaveasfilename(defaultextension=".map")
		self.onSave()

	def onClose(self):
		if self.space.saved == 1 or askokcancel("Unsaved changes", "Do you really wish to quit without saving?"):
			self.space.elements = []
			self.space.selection = []
			self.clipboard = []
			self.camera = Vec2(0,0)
			self.space.saved = 1

	def onRedraw(self,event):
		self.update()
		
	def onWindowClose(self):
		if self.space.saved == 1 or askokcancel("Unsaved changes", "Do you really wish to quit without saving?"):
			self.root.destroy()
		
	def catch_exception(self, *args):
		err = format_exception(*args)
		print err
		showerror("Unhandled Exception", err)

Application()
