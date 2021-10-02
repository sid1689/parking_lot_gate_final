from copy import copy
from datetime import datetime

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)

WEBCAM = 0
#The address to access the cameras below refers to analog camera models
GATE_CAMERA_1 = 'rtsp://login:password@IP1:RTSP_PORT/cam/realmonitor?channel=x'
GATE_CAMERA_2 = 'rtsp://login:password@IP2:RTSP_PORT/cam/realmonitor?channel=y'
GATE_CAMERA_3 = 'rtsp://login:password@IP3:RTSP_PORT/cam/realmonitor?channel=z'

FACES_PATH = "faces/"

def gbr_to_rgb(image):
    return image[:, :, ::-1]

# Em coordenadas x e y - ex: retangulo a começa na posição 2 e o retangulo b na posição 1 E (and) o retangulo a 
# termina na posição 4 e o b na 5, isso indica que o retangulo a está dentro de b 
def is_rectangle_inside(rectangle_a, rectangle_b):
    return rectangle_a.position > rectangle_b.position \
		and rectangle_a.end_point < rectangle_b.end_point

def current_datetime_as_string():
	now = datetime.now()
	return str(now.strftime("%d-%m-%Y_%H-%M-%S"))

def subimage(image, x_span, y_span):
	return image[y_span[0] : y_span[1], x_span[0] : x_span[1]]

def expand_rectangle(rectangle, factor, convert_to_int = False):
	old_center_point = copy(rectangle.center_point)

	rectangle.size *= factor

	if convert_to_int:
		rectangle.size = rectangle.size.to_int()

	rectangle.center_point = old_center_point
