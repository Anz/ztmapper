from Tkinter import *
from vec2 import *
from space import *
from util import *

class Editor:
	def __init__(self, canvas, images):
		self.canvas = canvas
		self.camera = Vec2(0,0)
		self.images = images

	def getScreenInSpace(self,vector):
		return screen2space(vector, self.camera, Vec2(self.canvas.winfo_width(), self.canvas.winfo_height()))

	def render(self, space):
		repaint(self.canvas, self.camera, self.images, space)

def repaint(canvas, camera, images, space):
	elements = space.elements
	selection = space.selection

	renderables = sorted(list(elements), key=sortElement)
	canvas.delete(ALL)

	screen = Vec2(canvas.winfo_width(), canvas.winfo_height())

	paintHelperline(canvas, camera, screen)
			
	for element in renderables:
		coordinate = space2screen(element.pos, camera, screen)
		image = images[element.type]
		canvas.create_image(coordinate.x, coordinate.y, image=image)

	for selected in selection:
		if 0 <= selected and selected < len(elements):
			element = elements[selected]
			image = images[element.type]
			coordinate = space2screen(element.pos, camera, screen)
			size = Vec2(image.width(), image.height()) / Vec2(2,2)
			tl = coordinate - size
			br = coordinate + size
			canvas.create_rectangle(tl.x, tl.y, br.x, br.y, fill=None, outline="yellow")
			

def paintHelperline(canvas, camera, screen):
	origin = space2screen(Vec2(0,0), camera, screen)
	w = canvas.winfo_width()
	h = canvas.winfo_height()

	screen_origin = screen2space(Vec2(0,0), camera, screen)
	helpline_step = 25
	helpline_offset = Vec2(helpline_step,screen_origin.y % helpline_step) - Vec2(screen_origin.x % helpline_step, 0)
	
	for i in range(w / helpline_step + 1):
		x = helpline_offset.x + helpline_step * i
		if screen2space(Vec2(x,0), camera, screen).x != 0:
			canvas.create_line(x, 0, x, h, fill="grey")
			
	for i in range(h / helpline_step + 1):
		y = helpline_offset.y + helpline_step * i
		if screen2space(Vec2(0,y), camera, screen).y != 0:
			canvas.create_line(0, y, w, y, fill="grey")
	
	helpline_step = 150
	helpline_offset = Vec2(helpline_step,screen_origin.y % helpline_step) - Vec2(screen_origin.x % helpline_step, 0)
	for i in range(w / helpline_step + 1):
		x = helpline_offset.x + helpline_step * i
		if screen2space(Vec2(x,0), camera, screen).x != 0:
			canvas.create_line(x, 0, x, h, fill="black", width=2)
			
	for i in range(h / helpline_step + 1):
		y = helpline_offset.y + helpline_step * i
		if screen2space(Vec2(0,y), camera, screen).y != 0:
			canvas.create_line(0, y, w, y, fill="black", width=2)
			
	canvas.create_line(0, origin.y, w, origin.y, fill="yellow")
	canvas.create_line(origin.x, 0, origin.x, h, fill="yellow")
