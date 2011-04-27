from Tkinter import *
from camera import *
from util import *

class Vec2:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def add(self,vector):
		self.x += vector.x
		self.y += vector.y
		return self

	def sub(self,vector):
		self.x -= vector.x
		self.y -= vector.y
		return self

	def mul(self,vector):
		self.x *= vector.x
		self.y *= vector.y
		return self

def vec2_copy(vector):
	return Vec2(vector.x, vector.y)

def space2screen(coordinate, camera, screen):
	point = vec2_copy(coordinate).mul(Vec2(1,-1))
	point.sub(vec2_copy(camera).mul(Vec2(1,-1)))
	point.add(vec2_copy(screen).mul(Vec2(0.5, 0.5)))
	return point

def repaint(canvas, camera, elements, selected):
	renderables = sorted(list(elements), key=sortElement)
	canvas.delete(ALL)

	x = -camera.x
	y = camera.y
	w = canvas.winfo_width()
	h = canvas.winfo_height()

	canvas.create_line(0, h / 2 + y, w, h / 2 + y, fill="red", dash=(4, 4))
	canvas.create_line(w / 2 + x, 0, w / 2 + x, h, fill="red", dash=(4, 4))

	cam = Vec2(camera.x, camera.y)
	screen = Vec2(canvas.winfo_width(), canvas.winfo_height())

	for element in renderables:
		coordinate = space2screen(Vec2(element.x, element.y), cam, screen)
		canvas.create_image(coordinate.x, coordinate.y, image=element.image)

	if 0 < selected and selected < len(elements):
		element = elements[selected]

		coordinate = space2screen(Vec2(element.x, element.y), cam, screen)
		size = Vec2(element.image.width(), element.image.height()).mul(Vec2(0.5, 0.5))
		tl = vec2_copy(coordinate).sub(size)
		br = vec2_copy(coordinate).add(size)
		canvas.create_rectangle(tl.x, tl.y, br.x, br.y, fill=None, outline="yellow")

