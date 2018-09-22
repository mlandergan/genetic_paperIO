import cv2
import numpy as np
from math import pi
import color_thresholds as th


CELL_SIZE = 30 # Size of each grid cell in pixels

class GameState():

    grid = []
    
    def __init__(self, player_color):
        self.player_color = player_color

    def update(self, img):

##        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
##        bounds = th.getPlayerBounds(self.player_color)
##        player_mask = cv2.inRange(hsv, bounds[0], bounds[1])

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 255)
        lines = cv2.HoughLinesP(edges, 1, pi/2, 2, None, 30, 1);

        x_offset = 0
        x_count = 0
        y_offset = 0
        y_count = 0
        
        for line in lines:
            pt1 = (line[0][0],line[0][1])
            pt2 = (line[0][2],line[0][3])

            if (pt1[0]-pt2[0] != 0):
                slope = (pt1[1]-pt2[1])/(pt1[0]-pt2[0])
            else:
                slope = 1000

            if slope > 100: # Vertical
                y_offset += (pt1[1] % CELL_SIZE)
                y_offset += (pt2[1] % CELL_SIZE)
                y_count += 2
                #cv2.line(img, pt1, pt2, (0,0,255), 3)
            elif slope < 1: # Horizontal
                x_offset += (pt1[0] % CELL_SIZE)
                x_offset += (pt2[0] % CELL_SIZE)
                x_count += 2
        #cv2.imshow("Lines", img)

        x_offset = int(x_offset / x_count)
        y_offset = int(y_offset / y_count)
        
        del self.grid[:]

        height = int((img.shape[0] - y_offset) / CELL_SIZE)
        width = int((img.shape[1] - x_offset) / CELL_SIZE)

        for y in range(height):
            self.grid.append([])
            for x in range(width):
                cell = img[y_offset + y*CELL_SIZE:y_offset + (y+1)*CELL_SIZE,
                           x_offset + x*CELL_SIZE:x_offset + (x+1)*CELL_SIZE, :]
                self.grid[y].append(np.mean(np.mean(cell, axis=0), axis=0))
                
    def showGrid(self):
        image = np.zeros((len(self.grid) * CELL_SIZE, len(self.grid[0]) * CELL_SIZE, 3), np.uint8)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cv2.rectangle(image, (x*CELL_SIZE, y*CELL_SIZE), ((x+1)*CELL_SIZE,(y+1)*CELL_SIZE), self.grid[y][x], -1)
        cv2.imshow('Grid', image)
        cv2.waitKey(0)
        

        
