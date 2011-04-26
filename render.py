from Tkinter import *

def repaint(canvas, elements, selected):
	canvas.delete(ALL)
	for element in elements:
		canvas.create_image(element.x, element.y, image=element.image)

	if len(elements) > selected:
		element = elements[selected]
		x = element.x - element.image.width() / 2
		y = element.y - element.image.height() / 2
		width = x + element.image.width()
		height = y + element.image.height()
		canvas.create_rectangle(x, y, width, height, fill=None, outline="yellow")

