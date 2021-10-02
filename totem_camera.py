from datetime import datetime
from math import ceil
import os
import re
import time

import cv2
import face_recognition
from numpy.lib.function_base import diff

from gate_camera import GateCamera
from utils import FACES_PATH, current_datetime_as_string

class TotemCamera(GateCamera):
	"""
	Represents a camera at a totem.
	"""
	
	FILE_REGEX = r"(.+)_0\.(.+)"

	def __init__(self, camera_address):
		super().__init__(camera_address)
	
	def _find_face(self):
		face = face_recognition.face_encodings(self._face)[0]
		start_time = time.time()
		distances = dict()

		for file in os.listdir(FACES_PATH):
			if not re.search(TotemCamera.FILE_REGEX, file):
				continue

			other_face = cv2.imread(FACES_PATH + file)
			other_face = face_recognition.face_encodings(other_face)[0]
			distance = face_recognition.face_distance([face], other_face)
			if distance <= 0.4:
				distances[FACES_PATH + file] = distance
		
		if not distances:
			print("Cliente não encontrado.")
			print("Process finished --- %s seconds ---" % (time.time() - start_time))
			return

		face_file = min(distances, key=distances.get)
		#print("distancia: ", distances[face_file])
		timestamp, extension = re.search(TotemCamera.FILE_REGEX, face_file).groups()
		file_datetime = datetime.strptime(timestamp, FACES_PATH + '%d-%m-%Y_%H-%M-%S')
		totem_datetime = datetime.now()
		difference = (totem_datetime - file_datetime).total_seconds() / 60
		if difference < 15:
			price = 0
		elif difference < 30:
			price = 1
		elif difference < 60:
			price = 2
		else:
			price = 4 + (ceil(difference / 60) - 1)* 2 
		new_name = FACES_PATH + current_datetime_as_string()
		os.rename(f"{face_file}", f"{new_name}_1.{extension}")
		print(f"Tempo de permanencia: {difference} minutos")
		print(f"Total: R$ {price}")
		print("Pagamento Realizado")
		print("Process finished --- %s seconds ---" % (time.time() - start_time))
		self._gate_open = True

	def _on_face_cropped(self):
		self._find_face()

