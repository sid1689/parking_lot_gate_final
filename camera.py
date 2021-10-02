import cv2
from vector import Vector

class Camera:
	camera_exists = False

	def __init__(self, camera):
		assert not Camera.camera_exists
		self._video_capture = cv2.VideoCapture(camera)

		Camera.camera_exists = True
	
	def stop(self):
		self._video_capture.release()

	@property
	def frame(self):
		(_, frame) = self._video_capture.read()
		return frame

	@property
	def size(self):
		x = self.frame.shape[1]
		y = self.frame.shape[0]
		
		return Vector(x, y)
