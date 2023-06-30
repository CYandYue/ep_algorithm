#!/usr/bin/env python3
# encoding: utf-8
import rospy
from geometry_msgs.msg import Twist
from robomaster import robot

import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

''' macro '''
X_VAL = 0.2
Y_VAL = 0.2
YAW_VAL = 20

msg = """
Control ep:
---------------------------
Moving around:
   q    w    e
   a    s    d
CTRL-C to quit
"""
e = """
Communications Failed
"""

''' read key inputs '''
def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = rospy.get_time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


''' main '''
if __name__ == "__main__":
    # init robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")
    ep_chassis = ep_robot.chassis

    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    try:
        while not rospy.is_shutdown():
            key = getKey()
            # ws是沿x的前后运动
            if key == 'w':
                ep_chassis.move(x=X_VAL, y=0, z=0, xy_speed=0.7).wait_for_completed()
            elif key == 's':
                ep_chassis.move(x=-X_VAL, y=0, z=0, xy_speed=0.7).wait_for_completed()
            # qe控制原地转向
            elif key == 'q':
                ep_chassis.move(x=0, y=0, z=YAW_VAL, z_speed=45).wait_for_completed()
            elif key == 'e':
                ep_chassis.move(x=0, y=0, z=-YAW_VAL, z_speed=45).wait_for_completed()              
            # ad控制横移
            elif key == 'a':
                ep_chassis.move(x=0, y=-Y_VAL, z=0, xy_speed=0.7).wait_for_completed()
            elif key == 'd':
                ep_chassis.move(x=0, y=Y_VAL, z=0, xy_speed=0.7).wait_for_completed()

            else:
                if (key == '\x03'):
                    break

    except:
        print(e)

    finally:
        print("once")


    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
