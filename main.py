from Tkinter import *
from tkFileDialog import *
from element import *
from image import *
from render import *
from level import *
from io import *

images = None
elements = []
curelement = 0
itemlist = None
canvas = None
statusbar = None
selector = 0

def refreshStatusbar(element):
	global curelement
	statusbar.config(text="%s (ID %d) - Pos (%dpx, %dpx) Rot (%.0f cel) Size (%dpx, %dpx) Layer (%d%%)" % \
		(element.type, curelement, element.x, element.y, element.rotation, element.image.width(), element.image.height(), element.layer*100))

def onCreateElement(event):
	global itemlist
	global images
	global curelement
	if len(itemlist.curselection()) == 0:
		return
	type = itemlist.get(itemlist.curselection()[0])
	image = images[type]
	curelement = len(elements)
	
	element = Element(type, event.x, event.y, 0.0, image)
	elements.append(element)
	refreshStatusbar(element)
	repaint(canvas, elements, curelement)
	
def onSelectElement(event):
	global canvas
	global elements
	global curelement
	global selector
	i = 0

	matches = []

	for element in elements:
		minx = element.x - element.image.width() / 2
		maxx = minx + element.image.width()
		miny = element.y - element.image.height() / 2
		maxy = miny + element.image.height()
		if (minx < event.x) and (event.x < maxx) and \
			(miny < event.y) and (event.y < maxy):
				matches.append(i)
		i += 1

	if len(matches) == 0:
		curelement = -1
		return

	curelement = matches[selector % len(matches)]
	element = elements[curelement]
	refreshStatusbar(element)
	repaint(canvas, elements, curelement)
	selector += 1

def onMove(event):
	global canvas
	global curelement
	global elements

	if len(elements) <= curelement:
		return
	element = elements[curelement]
	if event.keysym == 'Left':
		curelement -= 1
		if curelement < 0:
			curelement = len(elements) -1
	elif event.keysym == 'Right':
		curelement += 1
		if curelement >= len(elements):
			curelement = 0
	elif event.char == 'w':
		element.y -= 10
	elif event.char == 's':
		element.y += 10
	elif event.char == 'a':
		element.x -= 10
	elif event.char == 'd':
		element.x += 10
	elif event.char == 'y':
		element.layer -= 0.01
		if element.layer < 0.0:
			element.layer = 0.0
	elif event.char == 'x':
		element.layer += 0.01
		if element.layer > 1.0:
			element.layer = 1.0
	refreshStatusbar(element)
	repaint(canvas, elements, curelement)

def onOpen():
	global canvas
	global elements
	global curelement
	global images
	path = askopenfilename(filetypes = [('ZTG Map File', '*.map')])
	print path
	f = open(path, 'r')
	mapRead(f, elements, images)
	f.close()
	curelement = 0
	repaint(canvas, elements, curelement)

def onSave():
	return

def onSaveAs():
	global elements
	f = asksaveasfile(mode='w', defaultextension=".map")
	if f != None:
		mapWrite(elements, f)
		f.close()

def main():
	root = Tk()
	root.title("ZTG Map Editor (ztmapper)")
	root.bind_all('<Key>', onMove)
	root.geometry("%dx%d%+d%+d" % (800, 500, 0, 0))

	global images
	images = loadImages()

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open", command=onOpen)
	filemenu.add_command(label="Save", command=onSave)
	filemenu.add_command(label="Save As", command=onSaveAs)
	menubar.add_cascade(label="File", menu=filemenu)
	root.config(menu=menubar)

	global statusbar
	statusbar = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
	statusbar.pack(side=BOTTOM, fill=X)

	global canvas 
	canvas = Canvas(root, bg = 'black')
	#canvas.grid(row=0, column=0)
	canvas.pack(side=LEFT, fill=BOTH, expand=1)
	canvas.bind('<Button-1>',  onSelectElement)
	canvas.bind('<Button-3>',  onCreateElement)

	global itemlist
	itemlist = Listbox(root)
	#itemlist.grid(row=0, column=1, sticky=N+S)
	itemlist.pack(side=RIGHT, fill=Y)
	for image in images:
		itemlist.insert(END, image)

	repaint(canvas, elements, 0)
	
	root.mainloop()
	
main()
