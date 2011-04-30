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
		
class Application:

	def __init__(self):
		self.space = Space()	
		#self.camera = Vec2(0,0)
		self.selector = 0
		self.clipboard = []
		self.multiselection = 0
		self.saved = 1

		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.onClose)
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
		self.root.bind_all('<Control-s>', self.onShortSave)
		self.root.bind_all('<Control-c>', self.onCopy)
		self.root.bind_all('<Control-v>', self.onPaste)

		self.images = loadImages()

		menubar = Menu(self.root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open", command=self.onOpen)
		filemenu.add_command(label="Save", command=self.onSave)
		filemenu.add_command(label="Save As", command=self.onSaveAs)
		menubar.add_cascade(label="File", menu=filemenu)
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Reset Camera", command=self.onCameraReset)
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

		workpanel = Frame(self.root)
		workpanel.pack(side=RIGHT, fill=Y)
		
		self.itemlist = Listbox(workpanel)
		self.itemlist.pack(side=TOP, fill=BOTH, expand=1)
		for image in self.images:
			self.itemlist.insert(END, image.title())
			
		infopanel = Frame(workpanel)
		infopanel.pack(side=BOTTOM)
		
		self.type = Entry(infopanel)
		self.type.grid(row=0, column=0, columnspan=3)
		Label(infopanel, text="X").grid(row=1, column=0, sticky=W)
		self.x = Entry(infopanel, width=4)
		self.x.grid(row=1, column=1)
		Label(infopanel, text="px").grid(row=1, column=2, sticky=W)
		Label(infopanel, text="Y").grid(row=2, column=0, sticky=W)
		self.y = Entry(infopanel, width=4)
		self.y.grid(row=2, column=1)
		Label(infopanel, text="px").grid(row=2, column=2, sticky=W)
		Label(infopanel, text="Rotation").grid(row=3, column=0, sticky=W)
		self.rotation = Entry(infopanel, width=4)
		self.rotation.grid(row=3, column=1)
		Label(infopanel, text="deg").grid(row=3, column=2, sticky=W)
		Label(infopanel, text="Layer").grid(row=4, column=0, sticky=W)
		self.layer = Entry(infopanel, width=4)
		self.layer.grid(row=4, column=1)
		Label(infopanel, text="%").grid(row=4, column=2, sticky=W)
			
		self.editframe = EditFrame(self.editor, self.space)

		self.root.update_idletasks()
		w=self.root.winfo_width()
		h=self.root.winfo_height()
		extraW=self.root.winfo_screenwidth()-w
		extraH=self.root.winfo_screenheight()-h
		self.root.geometry("%dx%d%+d%+d" % (w*2,h*2,extraW/4,extraH/4))
		self.root.update_idletasks()
		self.update()
		self.root.mainloop()
		
	def update(self):
		#repaint(self.canvas, self.editor.camera, self.space)
		self.editor.render(self.space)

		"""
		self.camstatus.config(text="Camera (%5d px, %5d px)" % (self.camera.x, self.camera.y))

		if len(self.selection) == 0 or self.selection[0] < 0 or self.selection[0] >= len(self.elements):
			return
		
		element = self.elements[self.selection[0]]
		
		self.type.delete(0, len(self.type.get()))
		self.type.insert(0, element.type.title())
		self.x.delete(0, len(self.x.get()))
		self.x.insert(0, str(element.pos.x))
		self.y.delete(0, len(self.y.get()))
		self.y.insert(0, str(element.pos.y))
		self.rotation.delete(0, len(self.rotation.get()))
		self.rotation.insert(0, str(element.rotation))
		self.layer.delete(0, len(self.layer.get()))
		self.layer.insert(0, str(int(element.layer * 100)))
		"""
		
	def onEdit(self, event):
		self.editframe.show(event.x_root, event.y_root)
		"""
		if len(self.itemlist.curselection()) == 0:
			return
		self.saved = 0
		type = self.itemlist.get(self.itemlist.curselection()[0]).lower()
		image = self.images[type]
		self.selection = [ len(self.elements) ]
		
		mouse = screen2space(Vec2(event.x, event.y), self.camera, Vec2(self.canvas.winfo_width(), self.canvas.winfo_height()))
		element = Element(type, mouse, 0.0, image)
		self.elements.append(element)
		self.update()
		"""
		
	def onSelect(self, event):
		self.editframe.unshow()

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
			"""
			minx = element.pos.x - element.image.width() / 2
			maxx = minx + element.image.width()
			miny = element.pos.y - element.image.height() / 2
			maxy = miny + element.image.height()
			mouse = screen2space(Vec2(event.x, event.y), self.editor.camera, Vec2(self.canvas.winfo_width(), self.canvas.winfo_height()))
			
			if (minx < mouse.x) and (mouse.x < maxx) and \
				(miny < mouse.y) and (mouse.y < maxy):
					matches.append(i)
			"""
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
		self.editor.camera += Vec2(self.lastx - event.x, event.y - self.lasty)
		self.update()
		self.lastx = event.x
		self.lasty = event.y

	def onMotion(self,event):
		"""
		mouse = screen2space(Vec2(event.x, event.y), self.space.camera.x,  Vec2(self.canvas.winfo_width(), self.canvas.winfo_height()))
		self.mousestatus.config(text="Mouse (%5d px, %5d px)" % (mouse.x, mouse.y))
		"""

	def onCameraReset(self):
		self.editor.camera = Vec2(0,0)
		self.update()
	
	def onLeft(self, event):
		self.saved = 0
		self.space.moveSelection(Vec2(-1,0))
		self.update()
	
	def onRight(self, event):
		self.saved = 0
		self.space.moveSelection(Vec2(1,0))
		self.update()

	def onUp(self, event):
		self.saved = 0
		self.space.moveSelection(Vec2(0,1))
		self.update()

	def onDown(self, event):
		self.saved = 0
		self.space.moveSelection(Vec2(0,-1))
		self.update()

	def onDelete(self, event):
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
		self.saved = 1
		self.update()

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

	def onRedraw(self,event):
		self.update()
		
	def onClose(self):
		if self.saved == 1 or askokcancel("Unsaved changes", "Do you really wish to quit without saving?"):
			self.root.destroy()
		
	def catch_exception(self, *args):
		err = format_exception(*args)
		print err
		showerror("Unhandled Exception", err)

Application()
