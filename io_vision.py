import numpy as np
import cv2
import os
from mss import mss
import time
import color_thresholds as th

wall_color = (0, 0, 255, 0) # RGB Color

def init():
    global sct, scoreboard_mask
    sct = mss()

    scoreboard_mask = cv2.imread(os.getcwd() + '\\' + 'scoreboard_mask.png', 0)
    #scoreboard_mask = 255 - cv2.cvtColor(scoreboard_mask, cv2.COLOR_RGB2BGR)
    #b_channel, g_channel, r_channel = cv2.split(scoreboard_mask)
    #alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50
    #scoreboard_mask = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

def run():
    # (X, Y, Width, Height) Box to capture
    mon = {'top': 65, 'left': 0, 'width': 1920, 'height': 975}

    while 1:
        start_time = time.time()
        img = np.array(sct.grab(mon))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        background_mask = 255 - cv2.inRange(hsv, th.lower[th.BACKGROUND], th.upper[th.BACKGROUND])
        wall_mask = 255 - cv2.inRange(hsv, th.lower[th.WALL], th.upper[th.WALL])

        result = cv2.bitwise_and(img, img, mask=scoreboard_mask)

        result = cv2.bitwise_and(result, result, mask=wall_mask)
        result = cv2.bitwise_and(result, result, mask=background_mask)

        indices = np.where(wall_mask==0)
        result[indices[0], indices[1], :] = wall_color # Red Walls

        cv2.imshow('Example', result)

        
        #Press 'Q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        # Print the frame rate (I get about 20 fps)
       # print (1 / (time.time() - start_time))




if __name__ == "__main__":
    init()
    run()
