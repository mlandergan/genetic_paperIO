import cv2
import numpy as np
from math import pi
import color_thresholds as th
from operator import itemgetter
from scipy.stats import mode


CELL_SIZE = 30 # Size of each grid cell in pixels

class GameState():

    grid = []
    grid_state = []
    
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

            #cv2.line(img, pt1, pt2, (0,0,255), 3)

            if slope > 100: # Vertical
                y_offset += (pt1[1] % CELL_SIZE)
                y_offset += (pt2[1] % CELL_SIZE)
                y_count += 2
            elif slope < 1: # Horizontal
                x_offset += (pt1[0] % CELL_SIZE)
                x_offset += (pt2[0] % CELL_SIZE)
                x_count += 2
        #cv2.imshow("Lines", img)

        if (x_count == 0 or y_count == 0):
            x_offset = 0
            y_offset = 0
        else:
            x_offset = int(x_offset / x_count)
            y_offset = int(y_offset / y_count)
        
        del self.grid[:]

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


        height = int((hsv.shape[0] - y_offset) / CELL_SIZE)
        width = int((hsv.shape[1] - x_offset) / CELL_SIZE)

        for y in range(height):
            self.grid.append([])
            for x in range(width):
                cell = hsv[y_offset + y*CELL_SIZE:y_offset + (y+1)*CELL_SIZE,
                           x_offset + x*CELL_SIZE:x_offset + (x+1)*CELL_SIZE, :]
                color = np.mean(np.mean(cell, axis=0), axis=0)
                if (color[2] <= 127): # Hard Value Filter 
                    color = np.array([0, 0, 0], dtype= "float64")
                self.grid[y].append(color)

    def evaluateGrid(self):

        

        bucket_threshold = 10
        
        colors = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                color = self.grid[y][x]
                if (not (color[0] == 0 and color[1] == 0 and color[2] == 0)):
                    colors.append([y, x, self.grid[y][x][0], self.grid[y][x][1], self.grid[y][x][2]])

        # Sort Colors by Hue Values
        colors_sorted = sorted(colors, key=itemgetter(2), reverse=True)
  
        split_points = []
        for i in range(len(colors_sorted)-1):
            derivative_hue = colors_sorted[i+1][2] - colors_sorted[i][2]
            #print (derivative_hue)
            if (derivative_hue <= -bucket_threshold):
                split_points.append(i) # End of that bucket

        split_points.append(len(colors_sorted)-1)

        color_buckets = self.splitColors(colors_sorted, split_points)

        #print (len(split_points))

       # for b in color_buckets:
         #   print ('\nNew Bucket')
          #  for c in b:
           #     print (c)

    def splitColors(self, colors_sorted, split_points):
        buckets = []

        for i in range(len(split_points)-1):
            buckets.append(colors_sorted[split_points[i]+1:split_points[i+1]])

        return buckets
                
    def showGrid(self):
        image = np.zeros((len(self.grid) * CELL_SIZE, len(self.grid[0]) * CELL_SIZE, 3), np.uint8)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cv2.rectangle(image, (x*CELL_SIZE, y*CELL_SIZE), ((x+1)*CELL_SIZE,(y+1)*CELL_SIZE), self.grid[y][x], -1)
        image_bgr = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imshow('Grid', image_bgr)
        

        
