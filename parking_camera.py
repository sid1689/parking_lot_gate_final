from abc import abstractmethod

import cv2

from camera import Camera
from face_detection import detect_faces
from image_window import display_image, read_key
from periodic_timer import PeriodicTimer
from rectangle import Rectangle
from utils import\
	BLUE, GREEN, RED, YELLOW,\
		expand_rectangle, is_rectangle_inside, subimage
from vector import Vector

class ParkingCamera:
	"""
	Represents a camera in the parking lot.
	"""

	_TARGET_WIDTH_FACTOR = 0.3
	_TARGET_HEIGHT_FACTOR = 0.4

	def __init__(self, camera_address):
		#self._name = name
		# Create the camera.
		self._camera = Camera(camera_address)
		self._create_target()
		# This controls when to stop the program.
		self._should_run = True

		# Stores the current image/frame from the camera.
		self._frame = None
		# The rectangle displayed around the face when it's detected.
		self._face_rectangle = None

		self.__can_take_picture = True

		self._capture_enabled = True
		self._capture_timer = PeriodicTimer(1, self.enable_capture)

		self._run()
		self._stop()
	
	def enable_capture(self):
		self._capture_enabled = True
	
	@property
	def _can_take_picture(self):
		return self.__can_take_picture
	
	@_can_take_picture.setter
	def _can_take_picture(self, value):
		self.__can_take_picture = value

		if not self.__can_take_picture:
			self._target.color = YELLOW
		else:
			self._target.color = BLUE
	
	def _run(self):
		self._capture_timer.start()
		
		while self._should_run:
			# Get a frame from the camera.
			# Instead of using a long name (self._camera.frame) use a short one (self._frame)
			self._frame = self._camera.frame

			if self._can_take_picture and self._capture_enabled:
				# the function _detect_face() is being called and its result will be stored in is_inside.
				there_is_face_and_is_inside = self._detect_face()

				if there_is_face_and_is_inside:
					# se for true entra aqui e face_frame pega uma cópia de frame que é o que a tela está mostrando atualmente.
					self._crop_face()
					self._can_take_picture = False
					self._on_face_cropped()
				
				self._capture_enabled = False

			# se um rosto for retornado ele desenhará um retângulo ao redor do rosto.
			if self._face_rectangle is not None:
				self._face_rectangle.draw(self._frame)
			
			# desenha o retângulo do target.
			self._target.draw(self._frame)

			# basicamente a função imshow do openCV para mostrar na tela o video.
			display_image(self._frame)
			self._handle_input()

	def _create_target(self):
		frame_size = self._camera.size

		# Calculate the width and height of the target.
		target_size = Vector(
			frame_size.x * ParkingCamera._TARGET_WIDTH_FACTOR,
			frame_size.y * ParkingCamera._TARGET_HEIGHT_FACTOR
		).to_int()

		# Create rectangle at an arbitrary position.
		self._target = Rectangle((0, 0), target_size, BLUE)
		# Use property "center_point" to center the rectangle
		# at the center of the screen.
		self._target.center_point = frame_size // 2
	
	def _detect_face(self):
		# An argument is what you send to a function when you call it. Ex: detect_faces(_frame).
		# Parameter is what a function receives when it's defined. Ex: def detect_faces(_frame).
		faces = detect_faces(self._frame)

		# Verfica se a lista não está vazia, se não estiver vazia é true.
		if not faces:
			self._face_rectangle = None
			return False

		# Se algum rosto for detectado, só o primeiro será guardado.
		self._face_rectangle = faces[0]
		is_inside = False

		# Se a função is_rectangle_inside for true entra no if e muda a cor pra verde e deixa is_inside true, 
		# se for falso entra no else e muda a cor pra vermelho
		# e no fim retorna o valor de is_inside baseado por onde entrou if ou else.
		if is_rectangle_inside(self._face_rectangle, self._target):
			self._face_rectangle.color = GREEN
			is_inside = True
		else:
			self._face_rectangle.color = RED

		return is_inside
	
	def _crop_face(self):
		# expande o rosto capturado pela ROI
		expand_rectangle(self._face_rectangle, 1.25, convert_to_int = True)

		# pega a imagem da tela toda que está salva em face_frame, depois pega a posição onde começa e termina o rosto em x
		# e onde começa a termina o rosto em y.
		self._face = subimage(
			self._frame,
			(self._face_rectangle.position.x, self._face_rectangle.end_point.x),
			(self._face_rectangle.position.y, self._face_rectangle.end_point.y)
		)

	def _handle_input(self):
		self._key = read_key()

		if self._key == ord('q'):
			self._should_run = False

	def _stop(self):
		self._camera.stop()
		self._capture_timer.stop()
		cv2.destroyAllWindows()
	
	@abstractmethod
	def _on_face_cropped(self):
		pass
