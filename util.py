from vec2 import *

def sortElement(element):
	return element.layer

def space2screen(coordinate, camera, screen):
	return (coordinate - camera) * Vec2(1,-1) + screen * Vec2(0.5, 0.5)

def screen2space(coordinate, camera, screen):
	return (camera - coordinate) * Vec2(1,-1) - screen * Vec2(0.5, 0.5)
