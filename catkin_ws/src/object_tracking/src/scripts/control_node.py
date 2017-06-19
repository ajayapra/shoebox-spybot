#!/usr/bin/env python
# BEGIN ALL
import sys, select, tty, termios
import rospy
import roslaunch
from std_msgs.msg import String

class getInput:
    def __init__(self):
        self.key_pressed = ''
        self.key_pub = rospy.Publisher("action_input", String, queue_size=1)
        self.rate = rospy.Rate(100)
        self.package    = 'object_tracking'
        self.executable = 'tracker_proto.py'
        self.count = 0
        self.toggle = 0
        self.node = roslaunch.core.Node(self.package, self.executable)
        rospy.loginfo('Input keystroke')
        try:
            while not rospy.is_shutdown():
                self.getKey()
                self.execute()
                self.rate.sleep()
        except rospy.ROSInterruptException:
            pass

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        self.key_pressed = sys.stdin.read(1)
        settings = termios.tcgetattr(sys.stdin)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def execute(self):
        if (self.key_pressed == 'q') or (self.key_pressed == 'Q'):
            rospy.signal_shutdown('Bye')
        elif (self.key_pressed == 'v') or (self.key_pressed == 'V'):
            self.toggle = self.toggle + (-1)**(self.count+2)
            self.count = self.count + 1

        if self.toggle:
            self.launch = roslaunch.scriptapi.ROSLaunch()
            self.launch.start()
            self.process = self.launch.launch(self.node)

        else:
            self.process.stop()

if __name__ == '__main__':
    rospy.init_node("control_node", anonymous=False)
    getInput()
