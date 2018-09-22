import numpy as np
import cv2
import os
from mss import mss
import time
import color_thresholds as th
from game_state import GameState
import pyautogui as auto

wall_color = (0, 0, 255, 0) # RGB Color

# (X, Y, Width, Height) Box to capture
mon = {'top': 71, 'left': 0, 'width': 1920, 'height': 1080-71-40}

LOC_START = (945, 540-mon['top']) # Center of Upper-Left Starting Square
LOC_START_BUTTON = (1045, 355)

def init():
    global sct, scoreboard_mask, state
    sct = mss()
    scoreboard_mask = cv2.imread(os.getcwd() + '\\' + 'scoreboard_mask.png', 0)
    # Starts Game Automatically. Comment out if you dont want your mouse to freak out lol
    #auto.moveTo(LOC_START_BUTTON)
    #auto.click()
    #time.sleep(1.75)
    player_color = getPlayerColor()
    state = GameState((30, 201, 212))#player_color)

    print ('Player Color: {}'.format(player_color))

def run():

    while 1:
        start_time = time.time()
        #img = np.array(sct.grab(mon))
        img = cv2.imread(os.getcwd() + '\\' + 'example_screen.png')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        background_mask = 255 - cv2.inRange(hsv, th.lower[th.BACKGROUND], th.upper[th.BACKGROUND])
        wall_mask = 255 - cv2.inRange(hsv, th.lower[th.WALL], th.upper[th.WALL])
        result = cv2.bitwise_and(img, img, mask=scoreboard_mask)
        result = cv2.bitwise_and(result, result, mask=wall_mask)
        result = cv2.bitwise_and(result, result, mask=background_mask)
        #indices = np.where(wall_mask==0)
       # result[indices[0], indices[1], :] = wall_color # Red Walls

        cv2.circle(result, LOC_START, 3, (0, 0, 255), -1)

        cv2.imshow('Example', result)

        state.update(result)
        state.showGrid()
        
        #Press 'Q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        cv2.waitKey(0)
        # Print the frame rate (I get about 20 fps)
       # print (1 / (time.time() - start_time))

#Samples a box in the corner of the player's intiial 3x3 area to determine the player's color
def getPlayerColor():
    sample_size = 4
    img = np.array(sct.grab(mon))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    sample_box = hsv[LOC_START[1]-sample_size:LOC_START[1]+sample_size, LOC_START[0]-sample_size:LOC_START[0]+sample_size]
    return np.mean(sample_box, axis=0)[0]


if __name__ == "__main__":
    init()
    run()
