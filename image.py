from os import *
from ImageTk import *

class Image:
	def __init__(self,width, height):
		self.width = width
		self.height = height

def loadImages():
	images = {}

	for image in listdir("img"):
		key = image.split(".")[0]
		images[key] = PhotoImage(file="img/" + image)

	return images
