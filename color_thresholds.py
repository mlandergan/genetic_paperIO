import numpy as np

BACKGROUND = 0
WALL = 1

lower = {
        BACKGROUND : np.array([90, 10, 175], dtype = "uint16"),
        WALL : np.array([97, 47, 158], dtype = "uint16")
        }

upper = {
    BACKGROUND : np.array([100, 40, 255], dtype = "uint16"),
    WALL : np.array([98, 48, 158], dtype = "uint16")
    }
