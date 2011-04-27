class Vec2:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def __iadd__(self,vector):
		self.x += vector.x
		self.y += vector.y
		return self

	def __add__(self,vector):
		return Vec2(self.x+vector.x, self.y+vector.y)

	def __isub__(self,vector):
		self.x -= vector.x
		self.y -= vector.y
		return self

	def __sub__(self,vector):
		return Vec2(self.x-vector.x, self.y-vector.y)

	def __imul__(self,vector):
		self.x *= vector.x
		self.y *= vector.y
		return self

	def __mul__(self,vector):
		return Vec2(self.x*vector.x, self.y*vector.y)

def vec2_copy(vector):
	return Vec2(vector.x, vector.y)
