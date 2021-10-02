from parking_camera import ParkingCamera

class GateCamera(ParkingCamera):
	"""
	Represents a camera at a gate.
	"""

	def __init__(self, camera_address):
		super().__init__(camera_address)
	
	@property
	def _gate_open(self):
		return not self._can_take_picture
	
	@_gate_open.setter
	def _gate_open(self, value):
		self._can_take_picture = not value

		if not self._can_take_picture:
			print("Cancela aberta.")
		else:
			print("Cancela fechada.")

	def _handle_input(self):
		super()._handle_input()

		if self._key == ord('c'):
			if self._gate_open:
				self._gate_open = False
