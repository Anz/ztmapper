from element import *

def mapWrite(elements, f):
	for element in elements:
		f.write("%s %d %d %.1f %.2f\n" % (unicode(element.type.lower()), element.x, element.y, element.rotation, element.layer))

def mapRead(f, elements, images):
	while len(elements) > 0:
		elements.pop()
	for line in f:
		tokens = line.split(" ")
		image = images[tokens[0].lower()]
		element = Element(tokens[0], int(tokens[1]), int(tokens[2]), float(tokens[4]), image)
		element.rotation = float(tokens[3])
		elements.append(element)
