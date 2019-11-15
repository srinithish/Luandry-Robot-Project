import os
import sys
import time


import numpy as np
from LaundryActions import LaundryActions
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
myLAct1 = LaundryActions(arm1, speed=100, mvacc=100, wait=False)
myLAct2 = LaundryActions(arm2, speed=100, mvacc=100, wait=False)


myLAct1.customGoHome(wait=False)
myLAct2.customGoHome(wait=True)

###fold 1

myLAct1.customGoHome(wait=False)
myLAct2.customGoHome(wait=True)
myLAct1.verticalPick([400,-240, -3, -180, 0, 0],{'z' :-100})
myLAct2.verticalPick([400, 250, -13, -180, 0, 0],{'z' : -100})
myLAct1.syncGripperActions([400,-240, -3, -180, 0, 0],20,arm2,[400, 250, -13, -180, 0, 0],20)
myLAct1.approach(z = 50)
myLAct2.approach(z = 50)
myLAct1.traverseWithPrevAttitude([400,0, 50])
myLAct2.traverseWithPrevAttitude([400,0, 50])
myLAct1.approach(z = -40)
myLAct2.approach(z = -40)
myLAct1.syncGripperActions([400,0, 10, -180, 0, 0],300,arm2,[400, 0,10, -180, 0, 0],300)
myLAct1.customGoHome(wait=False)
myLAct2.customGoHome(wait=True)


####fold 2
myLAct1.verticalPick([400,225, -3, -180, 0, 0],{'z' :-100})
myLAct2.verticalPick([400, -235, -13, -180, 0, 0],{'z' : -100})
myLAct1.syncGripperActions([400,225, -3, -180, 0, 0],20,arm2,[400, -235, -13, -180, 0, 0],20)
myLAct1.approach(z = 60)
myLAct2.approach(z = 60)
myLAct1.traverseWithPrevAttitude([400,0, 60])
myLAct2.traverseWithPrevAttitude([400,0, 60])
myLAct1.approach(z = -50)
myLAct2.approach(z = -50)
myLAct1.syncGripperActions([400,0, 10, -180, 0, 0],300,arm2,[400, 0,10, -180, 0, 0],300)


myLAct1.customGoHome(wait=False)
myLAct2.customGoHome(wait=True)
###template



###collar
for i in range(2):
    myLAct1.verticalPick([500,0,1, -180, 0, 0],{'z' :-100})
    myLAct1.syncGripperActions([500,0, 1, -180, 0, 0],20)
    myLAct1.approach(x = -175)
    myLAct1.syncGripperActions([325,0, 1, -180, 0, 0],300)
    myLAct1.approach(z = 100)



myLAct1.verticalPick([560,0, 100, -180, 0, 0],{'z' :0})
myLAct1.syncGripperActions([560,0, 100, -180, 0, 0],500)
myLAct1.approach(yaw = 90,wait = True)

myLAct1.approach(z = -100,wait = True)
myLAct1.holdObject(50,wait = True)
myLAct1.approach(z = 275,wait = True)
myLAct1.approach(x = -250,wait = True)
myLAct1.approach(z = -175,wait = True)
myLAct1.approach(x = -100,wait = True)
myLAct1.holdObject(400,wait = True)









arm1.set_position(400, 0, 300, -180, 0, 0, wait=False)

arm1.set_position(400, 100, 300, -180, 0, 0, wait=False)

arm1.set_position(400, 100, 200, -180, 0, 0, wait=False)
arm1.set_position(400, -100, 200, -180, 0, 0, wait=False)



arm2.set_position(400, 0, 300, -180, 0, 0, wait=False)

arm2.set_position(400, -100, 300, -180, 0, 0, wait=False)


arm2.set_position(400, -100, 200, -180, 0, 0, wait=False)
arm2.set_position(400, 100, 200, -180, 0, 0, wait=True)


arm1.set_gripper_position(500,wait = False)
arm2.set_gripper_position(500,wait = True)

prepareNoodles.myCkAct1.stir(50,3,wait = False)
prepareNoodles.myCkAct2.stir(50,3,wait = False)


#########










while True:
    print(time.time())
    pos = arm1.get_position()[1][:3]
    print(pos)
    testBool = np.array([pos]).astype('int') - np.array([400, 0, 300])
    if not np.any(testBool):
        break
    




