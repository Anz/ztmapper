from os import *
from PIL import ImageTk, Image
from Tkinter import *
import Image

def loadImages():
	images = {}

	for image in listdir("img"):
		key = image.split(".")[0].lower()
		images[key] = ImageTk.PhotoImage(Image.open("img/" + image))

	return images
