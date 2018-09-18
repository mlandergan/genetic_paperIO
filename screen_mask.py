import os
import cv2

image_name = 'example_screen.png'
scale  = 1

def run():
    file_name = os.getcwd() + '\\' + image_name
    img = cv2.imread(file_name)

    img = scale_image(img, 50)
    cv2.imshow('Example', img)


def scale_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image_resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image_resized



if __name__=="__main__":
    run()
