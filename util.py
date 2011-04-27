from vec2 import *

def sortElement(element):
	return element.layer

def space2screen(coordinate, camera, screen):
	return (coordinate - camera) * Vec2(1,-1) + screen / Vec2(2,2)

def screen2space(coordinate, camera, screen):
	return coordinate * Vec2(1,-1) + screen / Vec2(-2,2) + camera
