from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from traceback import *
from element import *
from image import *
from render import *
from level import *
from camera import *
from util import *
from io import *
		
class Application:

	def __init__(self):
		self.camera = Camera(0,0)
		self.elements = []
		self.curelement = 0
		self.selector = 0
		self.file = None
	
		self.root = Tk()
		self.root.report_callback_exception = self.catch_exception
		self.root.report_callback_exception = self.catch_exception
		self.root.title("ZTG Map Editor (ztmapper)")
		self.root.bind_all('w', self.onMoveTop)
		self.root.bind_all('a', self.onMoveLeft)
		self.root.bind_all('s', self.onMoveDown)
		self.root.bind_all('d', self.onMoveRight)
		self.root.bind_all('<Shift-W>', self.onMoveSlowTop)
		self.root.bind_all('<Shift-A>', self.onMoveSlowLeft)
		self.root.bind_all('<Shift-S>', self.onMoveSlowDown)
		self.root.bind_all('<Shift-D>', self.onMoveSlowRight)
		self.root.bind_all('x', self.onDecrLayer)
		self.root.bind_all('y', self.onIncrLayer)
		self.root.bind_all('<Delete>', self.onDeleteElement)
		self.root.bind_all('<Left>', self.onBackElement)
		self.root.bind_all('<Right>', self.onNextElement)
		#self.root.geometry("%dx%d%+d%+d" % (800, 500, 0, 0))

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

		self.canvas = Canvas(self.root, bg = 'gray10')
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
		self.canvas.bind('<Button-1>',  self.onSelectElement)
		self.canvas.bind('<Button-3>',  self.onCreateElement)
		self.canvas.bind('<B1-Motion>',  self.onCameraMove)

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
		repaint(self.canvas, self.camera, self.elements, self.curelement)
		
		self.camstatus.config(text="Camera (%5d px, %5d px)" % (self.camera.x, self.camera.y))
		
		if self.curelement < 0 or self.curelement >= len(self.elements):
			return
		
		element = self.elements[self.curelement]
		
		self.type.delete(0, len(self.type.get()))
		self.type.insert(0, element.type.title())
		self.x.delete(0, len(self.x.get()))
		self.x.insert(0, str(element.x))
		self.y.delete(0, len(self.y.get()))
		self.y.insert(0, str(element.y))
		self.rotation.delete(0, len(self.rotation.get()))
		self.rotation.insert(0, str(element.rotation))
		self.layer.delete(0, len(self.layer.get()))
		self.layer.insert(0, str(int(element.layer * 100)))

	def onCreateElement(self, event):
		if len(self.itemlist.curselection()) == 0:
			return
		type = self.itemlist.get(self.itemlist.curselection()[0]).lower()
		image = self.images[type]
		self.curelement = len(self.elements)
		
		element = Element(type, event.x + self.camera.x, event.y + self.camera.y, 0.0, image)
		self.elements.append(element)
		self.update()
		
	def onSelectElement(self, event):
		self.lastx = event.x
		self.lasty = event.y
		i = 0
		matches = []

		for element in self.elements:
			minx = element.x - element.image.width() / 2
			maxx = minx + element.image.width()
			miny = element.y - element.image.height() / 2
			maxy = miny + element.image.height()
			x = event.x + self.camera.x
			y = event.y + self.camera.y
			if (minx < x) and (x < maxx) and \
				(miny < y) and (y < maxy):
					matches.append(i)
			i += 1

		if len(matches) == 0:
			self.curelement = -1
			return

		self.curelement = matches[self.selector % len(matches)]
		element = self.elements[self.curelement]
		self.update()
		self.selector += 1
	
	def onCameraMove(self,event):
		self.camera.x += (self.lastx - event.x)
		self.camera.y -= (self.lasty - event.y)
		self.update()
		self.lastx = event.x
		self.lasty = event.y
	
	def onCameraReset(self):
		self.camera.x = 0
		self.camera.y = 0
		self.update()
	
	def onMoveLeft(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].x -= 10
			self.update()
	
	def onMoveRight(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].x += 10
			self.update()

	def onMoveTop(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].y -= 10
			self.update()			

	def onMoveDown(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].y += 10
			self.update()
			
	def onMoveSlowLeft(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].x -= 1
			self.update()
	
	def onMoveSlowRight(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].x += 1
			self.update()

	def onMoveSlowTop(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].y -= 1
			self.update()			

	def onMoveSlowDown(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].y += 1
			self.update()

	def onIncrLayer(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].layer += 0.01
			if self.elements[self.curelement].layer > 1.0:
				self.elements[self.curelement].layer = 1.0
			self.update()

	def onDecrLayer(self, event):
		if self.curelement < len(self.elements):
			self.elements[self.curelement].layer -= 0.01
			if self.elements[self.curelement].layer < 0.0:
				self.elements[self.curelement].layer = 0.0
			self.update()
	
	def onDeleteElement(self, event):
		if self.curelement < len(self.elements):
			del self.elements[self.curelement]
			self.onNextElement(None)
			self.update()
	
	def onBackElement(self,event):
		self.curelement -= 1
		if self.curelement < 0:
			self.curelement = len(self.elements) -1
		self.update()
	
	def onNextElement(self,event):
		self.curelement += 1
		if self.curelement >= len(self.elements):
			self.curelement = 0
		self.update()
	
	def onOpen(self):
		self.path = askopenfilename(filetypes = [('ZTG Map File', '*.map')])
		file = open(self.path, "r")
		mapRead(file, self.elements, self.images)
		file.close()
		curelement = 0
		element = self.elements[curelement]
		self.camera.x = 0
		self.camera.y = 0
		self.update()

	def onSave(self):
		if self.path != None:
			file = open(self.path, "w")
			mapWrite(self.elements, file)
			file.close()

	def onSaveAs(self):
		self.path = asksaveasfilename(defaultextension=".map")
		if self.path != None:
			file = open(self.path, "w")
			mapWrite(self.elements, file)
			file.close()

	def catch_exception(self, *args):
		err = format_exception(*args)
		print err
		showerror("Unhandled Exception", err)

Application()
