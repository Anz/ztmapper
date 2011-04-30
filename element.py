from vec2 import *

class Element:
	def __init__(self, type, position, layer, rotation):
		self.type = type
		self.pos = vec2_copy(position)
		self.rotation = rotation
		self.layer = layer

def element_copy(element):
	return Element(element.type, element.pos, element.layer, element.rotation)
