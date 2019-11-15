# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:16:00 2019

@author: GELab
"""

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




##global variables
armHandle1 = initialiseArms(ip1)
armHandle2 = initialiseArms(ip2)

myLAct1 = LaundryActions(armHandle1, speed=100, mvacc=100, wait=False)
myLAct2 = LaundryActions(armHandle2, speed=100, mvacc=100, wait=False)
        
def foldSleeves(keypointsForArm1,keypointsForArm2):
    
    """
    1 2
    1 2
    keypointsForArm1:  {1:,2:}
    keypointsForArm2:  {1:,2:}
    
    """
    midLine = {}
    
    
    ## finding the midpoints
    midLine['Arm1'] = (np.array(keypointsForArm1[1])+np.array(keypointsForArm1[2]))//2
    midLine['Arm2'] = (np.array(keypointsForArm2[1])+np.array(keypointsForArm2[2]))//2
    midLine['Arm1'] = midLine['Arm1'].tolist()
    midLine['Arm2'] = midLine['Arm2'].tolist()
    
    ####fold 2
    myLAct1.customGoHome(wait=True)
    myLAct2.customGoHome(wait=True)
    myLAct1.verticalPick(keypointsForArm1[2],{'z' :-100})
    myLAct2.verticalPick(keypointsForArm2[2],{'z' : -100})
    
    print(keypointsForArm1[2] , keypointsForArm2[2])
    myLAct1.syncGripperActions(keypointsForArm1[2],20,armHandle2,keypointsForArm2[2],20)
    
    
    myLAct1.approach(z = 50)
    myLAct2.approach(z = 50)
    
    midLine['Arm1'][2] = 50
    midLine['Arm2'][2] = 50
    myLAct1.traverseWithPrevAttitude(midLine['Arm1'][:3])
    myLAct2.traverseWithPrevAttitude(midLine['Arm2'][:3])
    
    myLAct1.approach(z = -40)
    myLAct2.approach(z = -40)
    
    
    
    ### 50 -40 = 10
    midLine['Arm1'][2] = 10
    midLine['Arm2'][2] = 10
    
    myLAct1.syncGripperActions(midLine['Arm1'],300,armHandle2,midLine['Arm2'],300)
    myLAct1.customGoHome(wait=False)
    myLAct2.customGoHome(wait=True)
    
    
    
    
    
    
    ###fold 1
    myLAct1.verticalPick(keypointsForArm1[1],{'z' :-100})
    myLAct2.verticalPick(keypointsForArm2[1],{'z' : -100})
    myLAct1.syncGripperActions(keypointsForArm1[1],20,armHandle2,keypointsForArm2[1],20)
    myLAct1.approach(z = 50)
    myLAct2.approach(z = 50)
    
    midLine['Arm1'][2] = 50
    midLine['Arm2'][2] = 50
    myLAct1.traverseWithPrevAttitude(midLine['Arm1'][:3])
    myLAct2.traverseWithPrevAttitude(midLine['Arm2'][:3])
    myLAct1.approach(z = -40)
    myLAct2.approach(z = -40)
    
     ### 50 -40 = 10
    midLine['Arm1'][2] = 10
    midLine['Arm2'][2] = 10
    myLAct1.syncGripperActions(midLine['Arm1'],300,armHandle2,midLine['Arm2'],300)
    myLAct1.customGoHome(wait=False)
    myLAct2.customGoHome(wait=True)
    
    return True



if __name__ == '__main__':
    
    
    keypointsForArm1 = {1:[400,225, -5, -180, 0, 0],2:[400,-240, -3, -180, 0, 0]}
    keypointsForArm2 = {1:[400, -235, -10, -180, 0, 0],2:[400, 250, -13, -180, 0, 0]}
    
    
    foldSleeves(keypointsForArm1,keypointsForArm2)
    myLAct1.customGoHome(wait=True)
    myLAct2.customGoHome(wait=True)
    pass
    
    



