# Include (Ton of stuff from the 254 repo)(MEMO: Declan's buisness)
import cv2
import time
import numpy as np

starttime = time.time()


# Their DisplayModes make sence, I don't quite understand how the enum is used, need to touch up on that.
class DisplayMode():
	DISP_MODE_RAW = 0
	DISP_MODE_THRESH = 1 # 1
	DISP_MODE_TARGETS = 0 # 2
	DISP_MODE_TARGETS_PLUS = 0 # 3

class TargetInfo():
	centroid_x = 0 
	Centroid_y = 0
	width = 0
	height = 0
	#  std::vector<cv::Point> points;
	# ????

	# Something I ended up ignoring in the rest of the script is the varible types they use,
	# They have lots of varibles types in their file(double, float, ect.), and I just ducktyped most of them

cap = cv2.VideoCapture(0)
# Added

def processImpl(w, h, texOut, mode , h_min, h_max, s_min, s_max, v_min, v_max):

	# Mode = DisplayMode

	ret, frame = cap.read()
	#  Added

	print("Image is " +  str(w) + " x " + str(h))
	print(h_min, h_max, s_min, s_max, v_min, v_max)
	t  = time.time() - starttime

	# input = cv2.Mat
	# They create a mat here, but the equivlent is a numpy array, 
	# Most of the mats are defined because ducktyping does not exist

	# which Dana seems to stray from / may not need

	# input.create(h, w, CV_8UC4)
	# Read above

	hsv = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB) # CV_RGBA2RGB
	hsv = cv2.cvtColor(hsv, cv2.COLOR_RGB2HSV) # CV_RGB2HSV

	t  = time.time() - starttime
	print("cvtColor() cost " + str(t))

	thresh = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))

	accepted_targets = [] # Perhaps a list?????
	#Currently not using rejected targets, but have noted where it is called
	targets = []
	# May work, if not throw the tuples into a numpy array
	# foo = np.array([x,y,z])
	t  = time.time() - starttime
	print("inRange() cost " + str(t))

	im2, contours, hirearchy =  cv2.findContours(thresh,1,3)
	# 	cv::RETR_EXTERNAL,
    #	cv::CHAIN_APPROX_TC89_KCOS
	#  Exact Same method they are using
	#  std::vector<TargetInfo> rejected_targets;

	for cnt in contours:

		#Convex_contour.clear()
		convex_contour = cv2.convexHull(cnt, False)
		#poly.clear()
		print("At here")

		if (cv2.isContourConvex(convex_contour)):

			print("Contour is convex")
			target = TargetInfo()

			bounding_rect = cv2.boundingRect(convex_contour)



			target.centroid_x = bounding_rect.y + bounding_rect.height
			# centroid Y is top of target because it changes shape as you move

			target.centroid_y = bounding_rect.y + bounding_rect.height
			print(bounding_rect.width)
			target.width = bounding_rect.width
			target.height = bounding_rect.height
			target.points = convex_contour

			kMinTargetWidth = 20;
			kMaxTargetWidth = 300;

			kMinTargetHeight = 6;
			kMaxTargetHeight = 60;

			if (target.width < kMinTargetWidth or target.width > kMaxTargetWidth or target.height < kMinTargetHeight or target.height < kMaxTargetHeight):
				print("Rejecting target due to shape : " + str(target.height) + " x " + str(target.width))
		    	#	They have a list of rejected vectors here, but I don't think that cv2 can make vector object
		    	# 	Add this vector to the list of rejected
		    	accepted_targets.append(target)
		    	
		    	# I dont think we need a return
		    	# get out of the if

		    # Filter based on shape

			kMaxWideness = 7.0

			kMinWideness = 1.5

			print("Checking for wideness...")
      		wideness = target.width / target.height

      		if (wideness < kMinWideness or wideness > kMaxWideness):

      			print("Rejecting target due to shape : " + str(wideness))

      			# Push to our rejeceted targets
      			#I dont think we need a return
      			accepted_targets.append(target)


	      	#Filter based on fullness
	      	
	      	kMinFullness = .45;
	      	
	      	kMaxFullness = .95;

	      	origonial_contour_area = cv2.contourArea(convex_contour)

	      	area = target.width * target.height * 1.0

	      	fullness = original_contour_area / area

	      	'''
	      	The few lines above are really intresting
	      	'''

	      	if (fullness < kMinFullness or fullness > kMaxFullness):

	      		print("Rejecting target due to fullness : ", str(fullness))

	      		#Push to rejected targets
	      		return

	      	#Found a target

	      	print("Found target at ", str(target.centroid_x), str(target.Centroid_y), str(target.width), str(target.height))
	      	#Push to our accepted targets

	      	accepted_targets.append(target)
	      	


	    #One tab down
	#Two tabs down

	t  = time.time() - starttime
	print("Contour analysis cost : ", str(t))


	kMaxOffset = 10 
	found = False

	i = 0
	while (found != True and i < len(accepted_targets)):
		j = 0 
		while(found != True and j < len(accepted_targets)):

			# If i = j
			# Contine
			# Don't know the use of this

			targetI = accepted_targets[i]

			targetJ = accepted_targets[j]

			offset = abs(targetI.centroid_x - targetJ.centroid_x)
			if (offset < kMaxOffset):

				# Unfortunently, ther is no conditional operator in Python, so this is my workaround
				if (targetI.Centroid_y > targetJ.Centroid_y):
					topTarget = targetI
				else:
					topTarget = targetJ

				if (targetI.Centroid_y < targetJ.Centroid_y):
					bottemTarget = targetI
				else:
					bottemTarget = targetJ

				#End of this
				if (topTarget.height > bottemTarget.height):

					targets.append(topTarget)
					found = True
					# Break?
					# Knowing Python, this SHOULD revert back to the next line

	t = time.time()

	# vis	

	if (mode.DISP_MODE_RAW == 1):

		vis = input
	elif(mode.DISP_MODE_RAW == 1):

		vis = cv2.cvtColor(thresh, CV_GRAY2RGBA)
	else:

		vis = input
		#Rendering!
		for target in targets:
			cv2.polylines(vis, target.points, True, (0, 112, 255), 3)
			cv2.circle(vis, (target.centroid_x, target.Centroid_y), 4, (255, 50, 255), 3)

	'''
	if (mode == DISP_MODE_TARGETS_PLUS):
		for target in rejected_targets:
			cv2.polylines(Stats for the targets)
	'''
	print("Creating vis costed ", time.time() - t)

	# Some openGL shenangins.
	'''
	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, texOut);
	t = getTimeMs();
	glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE,
	                vis.data);
	LOGD("glTexSubImage2D() costs %d ms", getTimeInterval(t));
	'''
	return targets

# At this point it turns into some gomeish
#
# Some android studio-related configuration, definitly don't need
# 
# The 'ProcessFrame()' function seems to take similar arguments as processImp(),
# However it just seems to be a glorification of processImp(), addition the output of the data that the team wants
#

'''
My own bit on viewing the images
'''
while (True):
	
	viewMode = DisplayMode()
	viewMode.DISP_MODE_THRESH = 0
	viewMode.DISP_MODE_TARGETS = 1
	# This is a little soupy from what they did, but like I said earlier I don't understand enums

	cv2.imshow( "Images", processImpl(w = 50, h = 50, texOut = 0, mode = viewMode , h_min = 25, h_max = 100, s_min = 10, s_max = 100, v_min = 0, v_max = 1000))


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
			







