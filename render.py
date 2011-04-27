from Tkinter import *
from camera import *
from vec2 import *
from util import *

def repaint(canvas, camera, elements, selected):
	renderables = sorted(list(elements), key=sortElement)
	canvas.delete(ALL)

	cam = Vec2(camera.x, camera.y)
	screen = Vec2(canvas.winfo_width(), canvas.winfo_height())

	origin = space2screen(Vec2(0,0), cam, screen)
	w = canvas.winfo_width()
	h = canvas.winfo_height()

	canvas.create_line(0, origin.y, w, origin.y, fill="red", dash=(4, 4))
	canvas.create_line(origin.x, 0, origin.x, h, fill="red", dash=(4, 4))


	for element in renderables:
		coordinate = space2screen(Vec2(element.x, element.y), cam, screen)
		canvas.create_image(coordinate.x, coordinate.y, image=element.image)

	if 0 <= selected and selected < len(elements):
		element = elements[selected]

		coordinate = space2screen(Vec2(element.x, element.y), cam, screen)
		size = Vec2(element.image.width(), element.image.height()) * Vec2(0.5, 0.5)
		tl = coordinate - size
		br = coordinate + size
		canvas.create_rectangle(tl.x, tl.y, br.x, br.y, fill=None, outline="yellow")

