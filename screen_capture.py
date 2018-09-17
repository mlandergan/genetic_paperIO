import numpy as np
import cv2
from mss import mss
import time

'''
You Need mms, numpy, and opencv-python
'''

# (X, Y, Width, Height) Box to capture
mon = {'top': 160, 'left': 160, 'width': 600, 'height': 400}

sct = mss()

while 1:
    start_time = time.time()
    img = np.array(sct.grab(mon))
    cv2.imshow('test', img)
    #Press 'Q' to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    # Print the frame rate (I get about 20 fps)
    #print (1 / (time.time() - start_time))

