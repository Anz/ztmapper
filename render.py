from Tkinter import *
from camera import *
from util import *

def repaint(canvas, camera, elements, selected):
	renderables = sorted(list(elements), key=sortElement)
	canvas.delete(ALL)

	x = -camera.x
	y = -camera.y
	w = canvas.winfo_width()
	h = canvas.winfo_height()

	canvas.create_line(0, h / 2 + y, w, h / 2 + y, fill="red", dash=(4, 4))
	canvas.create_line(w / 2 + x, 0, w / 2 + x, h, fill="red", dash=(4, 4))


	for element in renderables:
		canvas.create_image(element.x - camera.x, element.y  - camera.y, image=element.image)

	if 0 < selected and selected < len(elements):
		element = elements[selected]
		x = element.x - element.image.width() / 2 - camera.x
		y = element.y - element.image.height() / 2 - camera.y
		width = x + element.image.width()
		height = y + element.image.height()
		canvas.create_rectangle(x, y, width, height, fill=None, outline="yellow")

