import cv2

from gate_camera import GateCamera
from utils import FACES_PATH, current_datetime_as_string

class EntranceCamera(GateCamera):
	"""
	Represents the entrance gate camera.
	"""

	def __init__(self, camera_address):
		super().__init__(camera_address)
	
	def _save_face(self):
		cv2.imwrite(
			FACES_PATH + current_datetime_as_string() + "_0.png",
			self._face
		)

	def _on_face_cropped(self):
		self._save_face()
