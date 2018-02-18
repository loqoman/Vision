# Command line script to convert RGB to HSV color-space
# Worth noting that the saturation and value numbers returned are fairly trivial, and not computed
# This means that in reality, this script is best used to find the hue value for a RBG color, which is still a valid use.

import sys
import numpy as np
import cv2
 
blue = sys.argv[1]
green = sys.argv[2]
red = sys.argv[3]  

error = 10	# Whatever kind or error we want for our 'hue' value
 
color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
 
hue = hsv_color[0][0][0]
 
print("Lower bound is :"),
print("[" + str(hue-error) + ", 100, 100]\n")
 
print("Upper bound is :"),
print("[" + str(hue + error) + ", 255, 255]")