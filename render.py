from Tkinter import *
from camera import *

def repaint(canvas, camera, elements, selected):
	canvas.delete(ALL)
	for element in elements:
		canvas.create_image(element.x - camera.x, element.y  - camera.y, image=element.image)

	if selected < len(elements):
		element = elements[selected]
		x = element.x - element.image.width() / 2 - camera.x
		y = element.y - element.image.height() / 2 - camera.y
		width = x + element.image.width()
		height = y + element.image.height()
		canvas.create_rectangle(x, y, width, height, fill=None, outline="yellow")

