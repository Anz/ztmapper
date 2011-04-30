from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from traceback import *
from element import *
from image import *
from render import *
from level import *
from editframe import *
from util import *
from io import *
		
class Application:

	def __init__(self):
		self.camera = Vec2(0,0)
		self.elements = []
		self.selection = []
		self.clipboard = []
		self.multiselection = 0
		self.selector = 0
		self.saved = 1
	
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.onClose)
		self.root.report_callback_exception = self.catch_exception
		self.root.report_callback_exception = self.catch_exception
		self.root.title("ZTG Map Editor (ztmapper)")
		self.root.bind_all('<Expose>', self.onRedraw)
		self.root.bind_all('w', self.onMoveTop)
		self.root.bind_all('a', self.onMoveLeft)
		self.root.bind_all('s', self.onMoveDown)
		self.root.bind_all('d', self.onMoveRight)
		self.root.bind_all('W', self.onMoveTop)
		self.root.bind_all('A', self.onMoveLeft)
		self.root.bind_all('S', self.onMoveDown)
		self.root.bind_all('D', self.onMoveRight)
		self.root.bind_all('x', self.onDecrLayer)
		self.root.bind_all('y', self.onIncrLayer)
		self.root.bind_all('<Delete>', self.onDeleteElement)
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
		self.canvas.bind('<Button-1>',  self.onSelectElement)
		self.canvas.bind('<Button-3>',  self.onCreateElement)
		self.canvas.bind('<B1-Motion>',  self.onCameraMove)
		self.canvas.bind('<Motion>',  self.onMotion)

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
			
		self.editframe = EditFrame()

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
		repaint(self.canvas, self.camera, self.elements, self.selection)
		
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
		
	def onCreateElement(self, event):
		self.editframe.show(event.x_root, event.y_root)

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
		
	def onSelectElement(self, event):
		self.editframe.unshow()

		self.lastx = event.x
		self.lasty = event.y
		i = 0
		matches = []

		for element in self.elements:
			minx = element.pos.x - element.image.width() / 2
			maxx = minx + element.image.width()
			miny = element.pos.y - element.image.height() / 2
			maxy = miny + element.image.height()
			mouse = screen2space(Vec2(event.x, event.y), self.camera, Vec2(self.canvas.winfo_width(), self.canvas.winfo_height()))
			if (minx < mouse.x) and (mouse.x < maxx) and \
				(miny < mouse.y) and (mouse.y < maxy):
					matches.append(i)
			i += 1

		if len(matches) == 0:
			return
		if self.multiselection == 0:
			self.selection = [ matches[self.selector % len(matches)] ]
		else:
			for selected in matches:
				if selected in self.selection:
					self.selection.remove(selected)
				else:
					self.selection.append(selected)
			
		self.update()
		self.selector += 1
	
	def onCameraMove(self,event):
		self.camera.x += (self.lastx - event.x)
		self.camera.y -= (self.lasty - event.y)
		self.update()
		self.lastx = event.x
		self.lasty = event.y

	def onMotion(self,event):	
		mouse = screen2space(Vec2(event.x, event.y), Vec2(self.camera.x, self.camera.y), Vec2(self.canvas.winfo_width(), self.canvas.winfo_height()))
		self.mousestatus.config(text="Mouse (%5d px, %5d px)" % (mouse.x, mouse.y))

	def onCameraReset(self):
		self.camera.x = 0
		self.camera.y = 0
		self.update()
	
	def onMoveLeft(self, event):
		speed = 10
		
		if event.keysym == 'A':
			speed = 1
	
		for selected in self.selection:
			if selected < len(self.elements):
				self.elements[selected].pos.x -= speed
				self.saved = 0
		self.update()
	
	def onMoveRight(self, event):
		speed = 10
		
		if event.keysym == 'D':
			speed = 1
	
		for selected in self.selection:
			if selected < len(self.elements):
				self.elements[selected].pos.x += speed
				self.saved = 0
		self.update()

	def onMoveTop(self, event):
		speed = 10
		
		if event.keysym == 'W':
			speed = 1
	
		for selected in self.selection:
			if selected < len(self.elements):
				self.elements[selected].pos.y += speed
				self.saved = 0
		self.update()	

	def onMoveDown(self, event):
		speed = 10
		
		if event.keysym == 'S':
			speed = 1
	
		for selected in self.selection:
			if selected < len(self.elements):
				self.elements[selected].pos.y -= speed
				self.saved = 0
		self.update()

	def onIncrLayer(self, event):
		for selected in self.selection:
			if selected < len(self.elements):
				self.elements[selected].layer += 0.01
				self.saved = 0
				if self.elements[selected].layer > 1.0:
					self.elements[selected].layer = 1.0
		self.update()

	def onDecrLayer(self, event):
		for selected in self.selection:
			if selected < len(self.elements):
				self.elements[selected].layer -= 0.01
				self.saved = 0
				if self.elements[selected].layer < 0.0:
					self.elements[selected].layer = 0.0
		self.update()
	
	def onDeleteElement(self, event):
		selected_elements = []
		for selected in self.selection:
			if selected < len(self.elements):
				selected_elements.append(self.elements[selected])
				
		for element in selected_elements:
			self.elements.remove(element)
			self.saved = 0
		self.selection = []
		self.update()
	
	def onBackElement(self,event):
		if len(self.elements) == 0:
			self.selection = []
			return
		min = len(self.elements) - 1
		for selected in self.selection:
			if selected < min:
				min = selected
		self.selection = [ min - 1 ]
		if self.selection[0] < 0:
			self.selection[0] = len(self.elements) -1
		self.camera = self.elements[self.selection[0]].pos
		self.update()
	
	def onNextElement(self,event):
		if len(self.elements) == 0:
			self.selection = []
			return
		max = 0
		for selected in self.selection:
			if selected > max:
				max = selected
		self.selection = [ max + 1 ]
		if self.selection[0] >= len(self.elements):
			self.selection[0] = 0
		self.camera = self.elements[self.selection[0]].pos
		self.update()
		
	def onSelectAll(self,event):
		self.selection = range(len(self.elements))
		self.update()
		
	def onCopy(self,event):
		self.clipboard = list(self.selection)
		
	def onPaste(self,event):
		self.selection = range(len(self.elements), len(self.elements)+len(self.clipboard))
		for selected in self.clipboard:
			if 0 <= selected and selected < len(self.elements):
				element = element_copy(self.elements[selected])
				self.elements.append(element)
				self.saved = 0
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
		mapRead(file, self.elements, self.images)
		file.close()
		curelement = 0
		element = self.elements[curelement]
		self.camera.x = 0
		self.camera.y = 0
		self.saved = 1
		self.update()

	def onSave(self):
		if self.path != None and self.path != "":
			file = open(self.path, "w")
			mapWrite(self.elements, file)
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
