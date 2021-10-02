class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __repr__(self):
		return f"({self.x}, {self.y})"

	def __add__(self, other_vector):
		return Vector(self.x + other_vector.x, self.y + other_vector.y)

	def __sub__(self, other_vector):
		return Vector(self.x - other_vector.x, self.y - other_vector.y)

	def __mul__(self, k):
		return Vector(self.x * k, self.y * k)

	def __truediv__(self, k):
		return Vector(self.x / k, self.y / k)

	def __floordiv__(self, k):
		return Vector(self.x // k, self.y // k)
	
	def __gt__(self, other_vector):
		return self.x > other_vector.x and self.y > other_vector.y
	
	def to_tuple(self):
		return (self.x, self.y)

	def to_int(self):
		return Vector(int(self.x), int(self.y))
