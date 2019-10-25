import os
import sys
import time

from cookingActions import cookingActions
from cookingActions2 import cookingActions2
from mainActions import mainActions
from xarm.wrapper import XArmAPI
from configparser import ConfigParser

parser = ConfigParser()
parser.read('./robot1.conf')
ip1 = parser.get('xArm', 'ip')
parser.read('./robot2.conf')
ip2 = parser.get('xArm', 'ip')


def handle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
    # TODO：Do different processing according to the error code


def initialiseArms(ip):
    arm = XArmAPI(ip, do_not_open=True, is_radian=False)
    arm.register_error_warn_changed_callback(handle_err_warn_changed)
    arm.connect()
    # enable motion
    arm.motion_enable(enable=True)
    # set mode: position control mode
    arm.set_mode(0)
    # set state: sport state
    arm.set_state(state=0)
    return arm


arm1 = initialiseArms(ip1)
arm2 = initialiseArms(ip2)

## actions here
myCkAct1 = cookingActions(arm1, speed=1000, mvacc=1000, wait=True)
myCkAct2 = cookingActions(arm2, speed=1000, mvacc=1000, wait=True)

myCkAct1.customGoHome(wait=True)
myCkAct2.customGoHome(wait=True)

"""
switch the stove on
"""


def switchStoveOn():
    myCkAct1.customGoHome()

    arm1.set_position(499, -200, 250, -180, 0, 0, speed=100, mvacc=100, wait=True)
    arm1.set_position(yaw=-90, relative=True, wait=True, is_radian=False)
    arm1.set_position(pitch=54, relative=True, wait=True, is_radian=False)
    arm1.set_gripper_position(200, wait=True)
    myCkAct1.approach(z=-215)
    myCkAct1.approach(y=87)

    arm1.set_gripper_position(110, wait=True)

    code, angles = arm1.get_servo_angle(is_radian=False)

    angles1 = angles[:-1] + [angles[-1] + 270]

    arm1.set_servo_angle(angle=angles1,
                         speed=None, mvacc=None, mvtime=None, is_radian=False, wait=True)

    arm1.set_gripper_position(500, wait=True)

    arm1.set_servo_angle(angle=angles,
                         speed=None, mvacc=None, mvtime=None, is_radian=False, wait=True)

    arm1.set_gripper_position(500, wait=True)

    myCkAct1.traverseWithPrevAttitude(endPosOnlyList=[499, -150, 35])

    myCkAct1.approach(z=100)

    # myCkAct1.customGoHome()


"""
pick glass and pour

"""

#####robot 1

def pickGlassAndPour():

    #####robot 1
    # myCkAct1.customGoHome()

    myCkAct1.horizontalPick([293, -325, 50, -180, 0, 0], {'y': -100},
                            (900, 700))

    myCkAct1.traverseWithPrevAttitude([380, 0, 250])
    myCkAct1.pour(-100, speed=100, mvacc=20)

    myCkAct1.horizontalPlace([293, -325, 50, -180, 0, 0], {'y': -100}, 900)
    # myCkAct1.customGoHome()

    #####robot 2
    # myCkAct2.customGoHome()
    #
    # myCkAct2.horizontalPick([293, -325, 50, -180, 0, 0], {'y': -100},
    #                         (900, 700))
    # myCkAct2.approach(z=200)  ##use only for robot2
    # myCkAct2.traverseWithPrevAttitude([600, 0, 300])
    # myCkAct2.pour(-100, speed=100, mvacc=20)
    # myCkAct2.approach(x=-200)  ## use ony for robot1
    # myCkAct2.horizontalPlace([293, -325, 50, -180, 0, 0], {'y': -100}, 900)
    # # myCkAct2.customGoHome()


    # myCkAct2.horizontalPick([183,-325,50,-180,0,0],{'y':-100},
    #                                 (900,700))
    # myCkAct2.approach(z=200) ##use only for robot2
    # myCkAct2.traverseWithPrevAttitude([600,0,350])
    # myCkAct2.pour(-100,speed=100,mvacc=20)
    # myCkAct2.approach(x=-200) ## use ony for robot1
    # myCkAct2.horizontalPlace([183,-325,50,-180,0,0],{'y':-100},900)
    # myCkAct2.customGoHome()

"""
Add Flavor
"""
def sprinkleFlavor():
    # myCkAct1.customGoHome()

    myCkAct1.horizontalPick([130, -340, 50, -180, 0, 0],{'y': -100},
                            (440, 330),isHorizontal = True)

    myCkAct1.traverseWithPrevAttitude([400, 0, 400])
    myCkAct1.sprinkle(numTimes=1, tiltBy=150, speed=950, mvacc=400)
    myCkAct1.horizontalPlace([130, -340, 50, -180, 0, 0], {'y': -100}, 440)

    # myCkAct1.customGoHome()


"""
Sprinkle salt

"""

def sprinkleSalt():
    # myCkAct1.customGoHome()

    myCkAct1.horizontalPick([195, 340, 40, -180, 0, 0], {'y': 100},
                            (410, 330))

    myCkAct1.traverseWithPrevAttitude([400, 0, 400])
    myCkAct1.sprinkle(numTimes=1, tiltBy=105, speed=950, mvacc=400)
    myCkAct1.horizontalPlace([195, 340, 40, -180, 0, 0], {'y': 100}, 410)

    # myCkAct1.customGoHome()


"""
sprinkle pepper
"""


def sprinklePepper():
    # myCkAct1.customGoHome()

    myCkAct1.horizontalPick([260, 340, 40, -180, 0, 0], {'y': 100},
                            (410, 330),isHorizontal = True)

    myCkAct1.traverseWithPrevAttitude([400, 0, 400])
    myCkAct1.sprinkle(numTimes=2, tiltBy=105, speed=950, mvacc=400)
    myCkAct1.horizontalPlace([260, 340, 40, -180, 0, 0], {'y': 100}, 410)

    # myCkAct1.customGoHome()


"""
Sprinkle flakes
"""


def sprinkleFlakes():
    # myCkAct1.customGoHome()

    myCkAct1.horizontalPick([130, 340, 40, -180, 0, 0], {'y': 100},
                            (460, 330), isHorizontal = True)

    myCkAct1.traverseWithPrevAttitude([400, 0, 400])
    myCkAct1.sprinkle(numTimes=2, tiltBy=150, speed=950, mvacc=400)
    myCkAct1.horizontalPlace([130, 340, 40, -180, 0, 0], {'y': 100}, 460)

    # myCkAct1.customGoHome()



"""
Pick and place noodles
"""


def pickAndPlaceNoodles():
    # myCkAct2.customGoHome()

    # arm.set_position(510,-225,100,-180,0,0,speed = 100, mvacc = 100, wait = True)
    myCkAct2.verticalPick([195, 350, 50, -180, 0, 0], {'z': -200}, (300, 120))
    arm2.set_position(670, 0, 220, -180, 0, 0, wait=True)

    myCkAct2.releaseObject()
    # myCkAct2.customGoHome()


"""
hold the pan

"""


def holdPan():
    # myCkAct2.customGoHome()

    myCkAct2.releaseObject()
    arm2.set_position(500, 0, 130, -180, 0, 0, wait=True)
    myCkAct2.holdObject(200)


"""
Pick handle and stir
"""


def pickStirrerAndStir():
    myCkAct1.customGoHome()

    # arm.set_position(510,-225,100,-180,0,0,speed = 100, mvacc = 100, wait = True)
    myCkAct1.verticalPick([510, -225, 0, -180, 0, 0], {'z': -200}, (300, 0))

    myCkAct1._achieveHorizontalGripperPos([500, 0, 300, -180, 0, 0])
    myCkAct1.traverseWithPrevAttitude([500, 0, 450])

    myCkAct1.approach(z=-135)
    start_time = time.time()
    myCkAct1.stir(speed=350, radius=50, numTimes=30, wait=True)
    print(int(time.time() - start_time))

    ## get back to vertical position
    myCkAct1._achieveVerticalGripperPos([500, 0, 400, -180, 0, 0])

    myCkAct1.verticalPlace([510, -225, 0, -180, 0, 0], {'z': -200}, 300)

    myCkAct1.customGoHome()


def switchStoveOff():
    # myCkAct1.customGoHome()

    arm1.set_position(499, -200, 250, -180, 0, 0, speed=100, mvacc=100, wait=True)
    arm1.set_position(yaw=-90, relative=True, wait=True, is_radian=False)
    arm1.set_position(pitch=54, relative=True, wait=True, is_radian=False)
    arm1.set_gripper_position(200, wait=True)
    myCkAct1.approach(z=-215)

    arm1.set_gripper_position(500, wait=True)
    myCkAct1.approach(y=87)

    code, angles = arm1.get_servo_angle(is_radian=False)

    angles1 = angles[:-1] + [angles[-1] + 270]

    arm1.set_servo_angle(angle=angles1,
                         speed=None, mvacc=None, mvtime=None, is_radian=False, wait=True)

    arm1.set_gripper_position(110, wait=True)

    arm1.set_servo_angle(angle=angles,
                         speed=None, mvacc=None, mvtime=None, is_radian=False, wait=True)

    arm1.set_gripper_position(500, wait=True)

    myCkAct1.traverseWithPrevAttitude(endPosOnlyList=[499, -150, 35])

    myCkAct1.approach(z=100)

    myCkAct1.customGoHome()


"""
release pan and go back
"""


def releasePan():
    myCkAct2.releaseObject()
    myCkAct2.customGoHome()


if __name__ == '__main__':
    pass
