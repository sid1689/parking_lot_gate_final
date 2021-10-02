import cv2
from vector import Vector

class Rectangle:
	def __init__(self, position, size, color):
		self.position = position
		self.size = size
		self.color = color
		
	@property
	def x(self):
		return self.position.x

	@property
	def y(self):
		return self.position.y

	@property
	def width(self):
		return self.size.x

	@property
	def height(self):
		return self.size.y

	@property
	def end_point(self):
		return self.position + self.size
	
	def draw(self, image):
		cv2.rectangle(image, self.position.to_tuple(), self.end_point.to_tuple(), self.color, 1)

	@property
	def center_point(self):
		return self.position + self.size // 2
	
	@center_point.setter
	def center_point(self, value):
		self.position = value - self.size // 2
