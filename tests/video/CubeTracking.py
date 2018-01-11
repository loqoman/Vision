#	Long-standing file for cube tracking
#	WIP

'''
	Long-term, cube tracking is possilbe. It's going to be a challenge on 
	multiple fronts, with the 254 stuff going on, early in build season, having a cube at home,
	and research. I have been diagramming what a logic tree would look like for a cube tracker. 
	The current distinguishing feature that I have been looking at with the cube is its bright yellow color.
	I can easily distuinguish the yellow color, and break that up. With proper contour approximation you can then draw a polygon around it
	The INTENSE math comes in when you have to triangulate my position -> cube position -> Vault(Or any applicable target). 
	Said math will definitly involve transformation of 2D objects, depending on how intense it would be.
	More to come(Hopefull), especially times where I can take a cube home.

'''
import cv2
import time
import numpy as np

starttime = time.time()



cap = cv2.VideoCapture(0)
ret, frame = cap.read()
