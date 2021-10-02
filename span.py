class Span:
	def __init__(self, start, length):
		self.start = start
		self.length = length
	
	@property
	def end(self):
		return self.start + self.length
