from element import *

def mapWrite(elements, f):
	for element in elements:
		f.write("%s %d %d %.1f %.2f\n" % (element.type, element.x, element.y, element.rotation, element.layer))

def mapRead(f, elements, images):
	while len(elements) > 0:
		elements.pop()
	for line in f:
		tokens = line.split(" ")
		image = images[tokens[0]]
		element = Element(tokens[0], tokens[1], tokens[2], tokens[4], image)
		element.rotation = tokens[3]
		elements.append(element)
