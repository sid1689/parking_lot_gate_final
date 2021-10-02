from threading import Timer

class PeriodicTimer:
	def __init__(self, interval, callback):
		self.interval = interval
		self.callback = callback
	
	def start(self):
		self._reset()
		self.timer.start()

	def stop(self):
		self.timer.cancel()
		self.timer = None
	
	def _callback(self):
		self.callback()
		self.start()
		
	def _reset(self):
		self.timer = Timer(self.interval, self._callback)