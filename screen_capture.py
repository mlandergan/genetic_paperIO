import numpy as np
import cv2
from mss import mss
import time

'''
You Need mms, numpy, and opencv-python
'''

def init():
    global sct
    sct = mss()


def run():
    # (X, Y, Width, Height) Box to capture
    mon = {'top': 145, 'left': 0, 'width': 1920, 'height': 875}

    while 1:
        start_time = time.time()
        img = np.array(sct.grab(mon))
        cv2.imshow('test', img)
        #Press 'Q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        # Print the frame rate (I get about 20 fps)
       # print (1 / (time.time() - start_time))




if __name__ == "__main__":
    init()
    run()
