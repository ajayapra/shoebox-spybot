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
import std_msgs

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from object_tracking.msg import position

# global variables
global ang_control
global lin_control
global val_recieved

ang_control = 0.0
lin_control = 0.0
val_recieved = False


# define controller class
class Controller:

    # define init
    def __init__(self):
        # Detect position from OpenCV
        rospy.Subscriber('custom_chatter', position, self.callback)
        rospy.spin()

    # define callback
    def callback(self, data):
        global ang_control
        global lin_control
        global val_recieved

        # set value recieved flag
        val_recieved = True

        #reference = 0
        #P = 0.001

        ref_pos  = rospy.get_param("/P_control/ref_pos") #needs a point and a size
        ref_size = rospy.get_param("/P_control/ref_size")
        P_ang = rospy.get_param("/P_control/P_ang") #angular proportional controller
        P_lin = rospy.get_param("/P_control/P_lin") #linear proportional controller
	P_lin_hist = rospy.get_param("/P_control/P_lin_hist") #Hysterisis for linear controller
	P_ang_hist = rospy.get_param("/P_control/P_ang_hist") #Hysterisis for angular controller
	P_lin_sat = rospy.get_param("/P_control/P_lin_sat") #Saturation value for linear controller
	P_ang_sat = rospy.get_param("/P_control/P_ang_sat") #Saturation value for angular controller
        #Employ hysterisis for both controllers
        err_ang = ref_pos - data.x # 100 pix deadzone +-50 each side
        err_lin = ref_size - data.radius # <50 move forward, >70 move back

        # define publisher
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.loginfo('ref_pos: %s ref_size: %s err_lin: %s err_ang: %s data.x: %s data.radius: %s', ref_pos, ref_size, err_lin, err_ang, data.x, data.radius)

        #Angular control hysterisis
        if err_ang < (-1*P_ang_hist):
            err_ang = err_ang + P_ang_hist
        elif err_ang > P_ang_hist:
            err_ang = err_ang - P_ang_hist
        else:
            err_ang = 0

        #Linear control hysterisis
        if err_lin < (-1*P_lin_hist):
            err_lin = err_lin + P_lin_hist
        elif err_lin > P_lin_hist:
            err_lin = err_lin - P_lin_hist
        else:
            err_lin = 0

        #Implement controller saturation limits if needed using ROS params
	if abs(P_ang*err_ang) < P_ang_sat:
        	ang_control = P_ang*err_ang
	elif err_ang < 0:
		ang_control = -P_ang_sat
	else:
		ang_control = P_ang_sat

	if abs(P_lin*err_lin) < P_lin_sat:
        	lin_control = P_lin*err_lin
	elif err_lin < 0:
		lin_control = -P_lin_sat
	else:
		lin_control = P_lin_sat


        rospy.loginfo('ref_pos: %s | ref_size: %s | err_lin: %s | err_ang: %s | lin_control: %s | ang_control: %s ', ref_pos, ref_size, err_lin, err_ang, lin_control, ang_control)

        #Publish Velocities
        linear  = Vector3(lin_control, 0.0, 0.0)
        angular = Vector3(0.0, 0.0, ang_control)
        message = Twist(linear, angular)
        pub.publish(message)


# standard boilerplate
if __name__ == '__main__':
    while not rospy.is_shutdown():
        rospy.init_node('jackal_move', anonymous=True)
        try:
            c = Controller()
        except rospy.ROSInterruptException:
            pass
