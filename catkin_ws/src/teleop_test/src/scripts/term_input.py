#!/usr/bin/env python
# BEGIN ALL
import sys, select, tty, termios
import rospy
from std_msgs.msg import String

class getInput:
    def __init__(self):
        self.key_pressed = ''
        self.key_pub = rospy.Publisher("action_input", String, queue_size=1)
        self.rate = rospy.Rate(100)
        rospy.loginfo('Input keystroke')
        try:
            while not rospy.is_shutdown():
                self.getKey()
                self.input()
                self.rate.sleep()
        except rospy.ROSInterruptException:
            pass

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        self.key_pressed = sys.stdin.read(1)
        settings = termios.tcgetattr(sys.stdin)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def input(self):
        self.key_pub.publish(self.key_pressed)
        rospy.loginfo(self.key_pressed)
        self.key_pressed = ''

if __name__ == '__main__':
    rospy.init_node("keyboard_in", anonymous=False)
    getInput()
