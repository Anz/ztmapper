from vec2 import *

class Space:
	def __init__(self):
		self.elements = []
		self.selection = []
		self.mode = 0

	def getSelected(self):
		selecteds = []
		for selected in self.selection:
			selecteds.append(self.elements[selected])
		return selecteds
			
	def addElement(self, element):
		self.selection = [ len(self.elements) ]
		self.elements.append(element)

	def moveSelection(self, vector):
		for element in self.getSelected():
			element.pos += vector
	
	def deleteSelection(self):
		for element in self.getSelected():
			self.elements.remove(element)
		self.selection = []

	def previous(self):
		if len(self.elements) == 0:
			self.selection = []
			return

		if len(self.selection) == 0:
			self.selection = [ len(self.elements) - 1]
			return

		self.selection = [ min(self.selection) - 1 ]
		if self.selection[0] < 0:
			self.selection[0] = len(self.elements) - 1

	def next(self):
		if len(self.elements) == 0:
			self.selection = []
			return

		if len(self.selection) == 0:
			self.selection = [0]
			return

		self.selection = [ max(self.selection) + 1 ]
		if self.selection[0] >= len(self.elements):
			self.selection[0] = 0
