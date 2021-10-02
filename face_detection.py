import face_recognition

from rectangle import Rectangle
from utils import BLUE, gbr_to_rgb
from vector import Vector

def detect_faces(image):
    face_locations = face_recognition.face_locations(gbr_to_rgb(image))

    return [Rectangle(Vector(left, top), Vector(right - left, bottom - top), BLUE)
                for (top, right, bottom, left) in face_locations]
