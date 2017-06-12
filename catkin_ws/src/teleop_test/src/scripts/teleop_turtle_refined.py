#!/usr/bin/env python
# BEGIN ALL
#import sys, select, tty, termios
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

keyMsg = ""
term = 0

class teleop_move:
    def __init__(self):
        self.keyMsg = ''
        self.lin_msg = Vector3()
        self.ang_msg = Vector3()
        self.pub_msg = Twist()
        self.lin_vel = 0.5
        self.ang_vel = 0.05
        self.rate = rospy.Rate(5)
        self.move_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=1)
        rospy.loginfo("Gonna Navigate!")
        try:
            while not rospy.is_shutdown():
                global term
                if term == 0:
                    self.move_bot()
                    self.rate.sleep()
                else:
                    break

        except rospy.ROSInterruptException:
            pass

        finally:
            self.move_pub.publish(Twist())



    def key_callback(self, data):
        global keyMsg
        keyMsg = data.data
        print ("in key callback")
        rospy.loginfo("I heard key %s", data.data)
        self.action_sub.unregister()

    def move_bot(self):
        global keyMsg
        self.action_sub = rospy.Subscriber("/action_input", String, self.key_callback)
        if keyMsg == 'w' or keyMsg == 'W':
            self.lin_msg = Vector3(x=float(self.lin_vel), y=float(0.0), z=float(0.0))
            self.ang_msg = Vector3(x=float(0.0), y=float(0.0), z=float(0.0))
        elif keyMsg == 's' or keyMsg == 'S':
            self.lin_msg = Vector3(x=float(-self.lin_vel), y=float(0.0), z=float(0.0))
            self.ang_msg = Vector3(x=float(0.0), y=float(0.0), z=float(0.0))
        elif keyMsg == 'd' or keyMsg == 'D':
            self.lin_msg = Vector3(x=float(0.0), y=float(0.0), z=float(0.0))
            self.ang_msg = Vector3(x=float(0.0), y=float(0.0), z=float(-self.ang_vel))
        elif keyMsg == 'a' or keyMsg == 'A':
            self.lin_msg = Vector3(x=float(0.0), y=float(0.0), z=float(0.0))
            self.ang_msg = Vector3(x=float(0.0), y=float(0.0), z=float(self.ang_vel))
        elif keyMsg == 'o' or keyMsg == 'O':
            global term
            term = 1
        else:
            self.lin_msg = Vector3(x=float(0.0), y=float(0.0), z=float(0.0))
            self.ang_msg = Vector3(x=float(0.0), y=float(0.0), z=float(0.0))
        self.pub_msg = Twist(linear=self.lin_msg, angular=self.ang_msg)
        self.move_pub.publish(self.pub_msg)
        keyMsg = ''

if __name__ == '__main__':
    rospy.init_node("bot_mover", anonymous=False)
    teleop_move()
