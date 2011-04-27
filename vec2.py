class Vec2:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def add(self,vector):
		self.x += vector.x
		self.y += vector.y
		return self

	def sub(self,vector):
		self.x -= vector.x
		self.y -= vector.y
		return self

	def mul(self,vector):
		self.x *= vector.x
		self.y *= vector.y
		return self

def vec2_copy(vector):
	return Vec2(vector.x, vector.y)
