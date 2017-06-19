#!/usr/bin/env python

# publisher + subscriber that reads position msgs from
# camera and calculates movement

# Intro to Robotics - EE5900 - Spring 2017
#          Assignment #6

#       Project #6 Group #2
#            prithvi
#            Aswin
#        Akhil (Team Lead)
#
# Revision: v1.2

# define imports
import rospy
import cv2
import cv_bridge
import argparse
import numpy as np

from   sensor_msgs.msg import Image
from   collections     import deque
from   object_tracking.msg import position

# Publisher
def talker():
    # Node declaration. Publish x, y, and radius to topic: custom_chatter,
    # message class: position, and queue_size: 1.
    pub = rospy.Publisher('custom_chatter', position, queue_size=1)

    # Assigning message class, position to a variable.
    msg = position()
    # x-position is published to position.
    msg.x = int(x)
    # y-position is published to position.
    msg.y = int(y)
    # radius of object is published to position.
    # The jackal stops if the radius is too small or too large(for safety).
    if (int(radius) > 15) and (int(radius) < 180) and (int(x) < 610) and (int(x) > 30) and (int(y) < 450) and (int(y) > 30) : 
        msg.radius = int(radius)
    else:
        msg.radius = 60
    # Tells rospy the name of the node.
    rospy.loginfo(msg)
    # Publishes x, y, and radius values to the topic.
    pub.publish(msg)

# Initial declarations.
counter = 0
(dX, dY) = (0, 0)
direction = ""
pts = deque(maxlen=32)
radius = 0
x = 0
y = 0

# Object tracker class.
class Tracker:
    # Function to subscribe to the camera. 
    def __init__(self):
	# cvBridge is a ROS library that provides an interface between ROS
        # and OpenCV.
        self.bridge = cv_bridge.CvBridge()
        # Uncomment the following two lines to launch windows. 
        #cv2.namedWindow("window1", 1) 
        #cv2.namedWindow("window2", 1)

        # rospy subscribes to the image_raw topic to receive images.
        self.image_sb = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback)
    # Function to process the received images. 
    def image_callback(self, msg):
	global counter
	global dX
	global dY
	global direction
	global pts
	global radius
	global x
	global y
        # imgmsg_to_cv2 converts an image message pointer to an OpenCV
        # message. 
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        # cvtColor applies an adaptive threshold to an array.
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Yellow threshold
        # Uncomment the following 3 lines to use yellow as the detector.
        yellowLower = np.array([20, 130, 130], np.uint8)
        yellowUpper = np.array([30, 255, 255], np.uint8)
        mask = cv2.inRange(hsv, yellowLower, yellowUpper)

	# Blue threshold
        # Comment the following 3 lines if using yellow.
	#blueLower = np.array([110, 50, 50], np.uint8)
        #blueUpper = np.array([130, 255, 255], np.uint8)
        
        # cv2.inRange in HSV color space leaves us with a binary mask
        # representing where in the image the desired color is found.
        #mask = cv2.inRange(hsv, blueLower, blueUpper)        
        # A series of dilations and erosions to remove any small blobs left
        # in the mask.
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=6)
        masked = cv2.bitwise_and(image, image, mask=mask)
        # Uncomment the below two lines to view the camera image and the
        # masked image.
        #cv2.imshow("window1", image)
        #cv2.imshow("window2", masked)

        # Find contours in the mask and initialize the current center of
        # the object.
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

        # Proceed if at least one contour was found.
	if len(cnts) > 0:
            # Find the largest contour in the mask, then use it to 
            # compute the minimum enclosing circle and centroid.
	    c = max(cnts, key=cv2.contourArea)
	    ((x, y), radius) = cv2.minEnclosingCircle(c)
	    M = cv2.moments(c)
	    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Only proceed if the radius meets a minimum size.
	    if radius > 10:
                # Draw the circle and centroid on the frame,
                # then update the list of tracked points.
		cv2.circle(image, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
		cv2.circle(image, center, 5, (0, 0, 255), -1)
		pts.appendleft(center)
 
        # Loop over the set of tracked points.
       	for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore them.
	    if pts[i - 1] is None or pts[i] is None:
	        continue
       
            # check to see if enough points have been accumulated in
	    # the buffer
	    if counter >= 10 and i == 1 and pts[-10] is not None:
                # compute the difference between the x and y
		# coordinates and re-initialize the direction
		# text variables
	        dX = pts[-10][0] - pts[i][0]
	        dY = pts[-10][1] - pts[i][1]
	        (dirX, dirY) = ("", "")
                # ensure there is significant movement in the x direction.
	        if np.abs(dX) > 20:
	            dirX = "East" if np.sign(dX) == 1 else "West"
                # ensure there is significant movement in the x direction.
	        if np.abs(dY) > 20:
	            dirY = "North" if np.sign(dY) == 1 else "South"
                # handle when both directions are non-empty
	        if dirX != "" and dirY != "":
	            direction = "{}-{}".format(dirY, dirX)
                # otherwise, only one direction is non-empty
	        else:
    	            direction = dirX if dirX != "" else dirY
            
            # otherwise, compute the thickness of the line and 
            # draw the connecting lines.
	    thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
	    cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the movement deltas and the direction of movement on 
        # the frame.
	cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
	    0.65, (0, 0, 255), 3)
        # Calling the publisher.
	talker()
	cv2.putText(image, "x: {}, y: {}, rad: {}".format(int(x), int(y), int(radius)),
            (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)
        # Show the frame to the screen and increment the frame counter.
        # Uncomment the following line to view the frame.
	#cv2.imshow("window2", image)
        cv2.waitKey(3)
	counter += 1

# Initialize node.
rospy.init_node('Track_Marker')
Track_Marker = Tracker()
rospy.spin()


