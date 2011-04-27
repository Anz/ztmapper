from element import *

def mapWrite(elements, f):
	for element in elements:
		f.write("%s\t%d\t%d\t%.1f\t%.2f\n" % (unicode(element.type.lower()), element.x, element.y, element.layer, element.rotation))

def mapRead(f, elements, images):
	while len(elements) > 0:
		elements.pop()
	for line in f:
		tokens = line.split("\t")
		image = images[tokens[0].lower()]
		element = Element(tokens[0], int(tokens[1]), int(tokens[2]), float(tokens[3]), image)
		element.rotation = float(tokens[4])
		elements.append(element)
