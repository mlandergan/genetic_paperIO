import os
import cv2
import numpy as np

image_name = 'example_screen.png'

wall_color = (0, 0, 255)

color_background_lower = np.array([90, 10, 175], dtype = "uint16")
color_background_upper = np.array([100, 40, 255], dtype = "uint16")

color_wall_lower = np.array([97, 47, 158], dtype = "uint16")
color_wall_upper = np.array([98, 48, 158], dtype = "uint16")

def run():
    file_name = os.getcwd() + '\\' + image_name
    img = cv2.imread(file_name)

    #img = scale_image(img, 50)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    background_mask = cv2.inRange(hsv, color_background_lower, color_background_upper)
    wall_mask = 255 - cv2.inRange(hsv, color_wall_lower, color_wall_upper)

    result = cv2.bitwise_and(img, img, mask=wall_mask)
    indices = np.where(wall_mask==0)
    result[indices[0], indices[1], :] = wall_color
   # result = cv2.bitwise_and(result, result, mask=background_mask)

    cv2.imshow('Example', result)


def scale_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image_resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image_resized



if __name__=="__main__":
    run()
