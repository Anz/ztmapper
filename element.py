from vec2 import *

class Element:
	def __init__(self,type,pos,layer, image):
		self.type = type
		self.pos = vec2_copy(pos)
		self.rotation = 0.0
		self.layer = layer
		self.image = image

def element_copy(element):
	copy = Element(element.type, element.pos, element.layer, element.image)
	copy.rotation = element.rotation
	return copy