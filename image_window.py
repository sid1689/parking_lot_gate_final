import cv2

last_window_name = 'video'

def display_image(image, window_name = last_window_name):
    global last_window_name
    
    if window_name != last_window_name:
        last_window_name = window_name

    cv2.imshow(window_name, image)

def read_key(delay = 10):
    return cv2.waitKey(delay)
