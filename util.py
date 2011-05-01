from vec2 import *

def sortElement(element):
	return element.layer

def space2screen(coordinate, camera, screen):
	return (coordinate - camera) * Vec2(1,-1) + screen / Vec2(2,2)

def screen2space(coordinate, camera, screen):
	return coordinate * Vec2(1,-1) + screen / Vec2(-2,2) + camera

def overlapElements(element, elements, images):
	matches = []
	image = images[element.type]
	size = Vec2(image.width(), image.height())
	a = element.pos - size / Vec2(2,2)
	d = element.pos + size / Vec2(2,2)
	b = Vec2(a.x, d.y)
	c = Vec2(d.x, a.y)

	for compare in elements:
		image = images[compare.type]
		size = Vec2(image.width(), image.height())
		cmin = compare.pos - size / Vec2(2,2)
		cmax = compare.pos + size / Vec2(2,2)
		
		if (cmin < a and a < cmax) or \
		   (cmin < b and b < cmax) or \
	           (cmin < c and c < cmax) or \
	           (cmin < d and d < cmax):
			matches.append(compare)

	return matches
			
