from vec2 import *

def sortElement(element):
	return element.layer

def space2screen(coordinate, camera, screen):
	point = vec2_copy(coordinate).mul(Vec2(1,-1))
	point.sub(vec2_copy(camera).mul(Vec2(1,-1)))
	point.add(vec2_copy(screen).mul(Vec2(0.5, 0.5)))
	return point

def screen2space(coordinate, camera, screen):
	point = vec2_copy(screen).mul(Vec2(-0.5, -0.5))
	point.add(vec2_copy(camera).mul(Vec2(1,-1)))
	point.sub(vec2_copy(coordinate).mul(Vec2(1,-1)))
	return point

