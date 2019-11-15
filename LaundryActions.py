
"""
@author: nithish
"""

from xarm.wrapper import XArmAPI


# import numpy as np


class LaundryActions:

    def __init__(self, armHandle, **kwargs):

        """
        @params:
            armHandle : required
            
            wait: default True
            
            speed: default 100

            mvacc: default 100
        """

        self._armHandle = armHandle
        # TODO:check for sanity and coonection

        self._speed = kwargs.get('speed', 100)
        self._mvacc = kwargs.get('mvacc', 100)
        self._wait = kwargs.get('wait', True)
        self._currentAttitude = []
        pass

    def setStateAndConnect():
        pass

    def _getDefaults(self, **kwargs):
        
        """
        gets default speed,mvacc,wait if not passed or is None
        """

        speed = self._speed if kwargs.get('speed', None) is None else kwargs['speed']
        mvacc = self._mvacc if kwargs.get('mvacc', None) is None else kwargs['mvacc']
        wait = self._wait if kwargs.get('wait', None) is None else kwargs['wait']

        return speed, mvacc, wait

    def customGoHome(self,wait = True):

        armHandle = self._armHandle
        
        # TODO: convert to servo angle
        #        armHandle.set_mode(1)

        armHandle.set_servo_angle(angle = [0,-43.3,0,17.6,0,60.9,0],speed = 100,mvacc = 10,wait  = wait)

        #        armHandle.set_mode(0)
        # armHandle.set_position(250, 0, 150, -180, 0, 0,
        #                        speed=100, mvacc=10,
        #                        wait=True, is_radian=False)
        code = armHandle.set_gripper_mode(0)
        code = armHandle.set_gripper_enable(True)
        armHandle.set_gripper_position(450, wait=wait)

        pass

    def holdObject(self, value,speed=None, mvacc=None,wait = None):

        """
        holds the object with gripper value
        position: where the graipper value change to occur
        """
        
        
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        armHandle = self._armHandle
        

        armHandle.set_gripper_position(value, wait=wait)
        pass


    def _achieveHorizontalGripperPos(self, startPos,speed=None, mvacc=None, wait=None):

        """
        Takes in start position that it wants to reach and decides the attitude to be
        negative Y or positive y

        
        Always reaches 250,y,400 and performs action
        

        @params:
            startPos: [x,y,z,attituted] uses only to decide the direiton of change

        """

        armHandle = self._armHandle
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)

        if startPos[1] > 0:

            xRoll = -90
            y = 20

        ## if y is -ve
        elif startPos[1] <= 0:

            xRoll = 90
            y = -20

        ###a

        ## TODO : check these speeds and mvacc for valididty and change y if reqired
        armHandle.set_position(250, y, 400, -180, 90, 0, speed=speed, mvacc=mvacc, wait=wait,
                                is_radian=False)
        
        armHandle.set_position(250, y, 400, xRoll, 90, 0, speed=speed, mvacc=mvacc, wait=wait,
                               is_radian=False)
        
        ## return orientation
        
        self._currentAttitude = [xRoll, 90, 0]
        
        return self._currentAttitude

    def _achieveVerticalGripperPos(self, startPos,speed=None, mvacc=None, wait=None):

        """
        no use of start pos
        """

        armHandle = self._armHandle
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        ## TODO may require to do in joint angles
        armHandle.set_position(250, 0, 350, -180, 0, 0, speed=speed, mvacc=mvacc, wait=wait,
                               is_radian=False)
        
        
        self._currentAttitude = [-180, 0, 0]
        
        return self._currentAttitude

    def achieveAttitude(self):
        """
        could be used to dynamically orient to an object
        """

        pass

    def horizontalPick(self, objPos, approachAfterStart,
                       gripHoldValues,isHorizontal= False,
                       speed=None, mvacc=None, wait=None,ZoffGround = 25):

        """
        Achieves horizontal position first

        @params:
            objPos: where to standby for picking up the object
            endPos: the endpoint at where the object has to be placed

            approachAfterStart: dict of what movements to make relative {x:100,y:100}
            
            gripHoldValues: tuple(startGripper,endGripper)

            ZoffGround: amout z to be lifted
        """

        armHandle = self._armHandle

        ##speed, mvacc, wait overridden with defauls if not provided
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)

        ##horizaontal position achieved
        if not isHorizontal:
            self._achieveHorizontalGripperPos(objPos,speed=speed, mvacc=mvacc, wait=wait)
            
        
        
#        horizontalPosAngles = armHandle.get_position(is_radian=False)[1][3:]
        ##before gripper position
        horizontalPosAngles = self._currentAttitude
        self.holdObject(gripHoldValues[0],wait = wait)
        
#        armHandle.set_gripper_position(gripHoldValues[0], wait=True)
        ##reach obj pos - approach
        
        objPosCopy = list(objPos)
        objPosCopy[3:] = horizontalPosAngles
        objPosCopy[0] = objPos[0] - approachAfterStart.get('x',0) 
        objPosCopy[1] = objPos[1] - approachAfterStart.get('y',0) 
        objPosCopy[2] = objPos[2] - approachAfterStart.get('z',0) 
        
        print('pos',objPosCopy,'hori',horizontalPosAngles)
       
        
        ret = armHandle.set_position(*objPosCopy, speed=speed, mvacc=mvacc, wait=wait, is_radian=False)
        print('return value is : ',ret)
        ###approach the object
        self.approach(**approachAfterStart,speed=speed, mvacc=mvacc, wait=wait)

        ###hold the object
        
        return armHandle.get_position(is_radian=False)[1]

    def horizontalPlace(self, objPlacingPos, approachDirn,
                        gripHoldValue,
                        speed=None, mvacc=None, wait=None,ZoffGround = 25 ):

        """
        Always succeds a horizontal Pick
        Assumes object already held by gripper

        @params:
            objPlacingPos : position before approach

            approachEnd: dict of what movements to make relative {x:100,y:100}

        """
        armHandle = self._armHandle

        ##speed, mvacc, wait overridden with defauls if not provided
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)

        ### assumes horizontal Pick was performed
#        horizontalPosAngles = armHandle.get_position(is_radian=False)[1][3:]
        horizontalPosAngles = self._currentAttitude
        ## TODO: check for validity of horizontal gripper positions
        
        objPlacingPos[3:] = horizontalPosAngles
        objPlacingPos[0] = objPlacingPos[0] - approachDirn.get('x',0) 
        objPlacingPos[1] = objPlacingPos[1] - approachDirn.get('y',0) 
        objPlacingPos[2] = objPlacingPos[2] - approachDirn.get('z',0) + ZoffGround
        armHandle.set_position(*objPlacingPos, speed=speed, mvacc=mvacc, wait=wait, is_radian=False)

        ###approach the object
        self.approach(**approachDirn,speed=speed, mvacc=mvacc, wait=wait)
        
        
        ### decend by 25
        self.approach(z= -ZoffGround,speed=speed, mvacc=mvacc, wait=wait)

        ###release the object
#        self.holdObject(gripHoldValue,wait = wait)
        armHandle.set_gripper_position(gripHoldValue, wait=True)

        ###go back by approach

        reverseApproachAfterStart = {key: -value for key, value in approachDirn.items()}
        self.approach(**reverseApproachAfterStart,speed=speed, mvacc=mvacc, wait=wait)

        return armHandle.get_position(is_radian=False)[1]

    def verticalPick(self, objPickPos, approachDirn,
                     
                     speed=None, mvacc=None, wait=None):

        """
        Orientation should and change
        Overrides orienations

        @params:
            gripHoldValues = (before,after)
            
            objPickPos = [x...,yaw...] eact obj location
            
            approachDir= {x: value....}
        @return:

            current position list
        """

        armHandle = self._armHandle
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)

        ##over ridding orientations
        self._currentAttitude = [-180, 0, 0]
        ## TODO: Achieve vertical attitutde here through function
        
        
        objPickPosCopy = list(objPickPos)
        objPickPosCopy[3:] = self._currentAttitude
        
        objPickPosCopy[0] = objPickPosCopy[0] - approachDirn.get('x',0) 
        objPickPosCopy[1] = objPickPosCopy[1] - approachDirn.get('y',0) 
        objPickPosCopy[2] = objPickPosCopy[2] - approachDirn.get('z',0) 
        armHandle.set_position(*objPickPosCopy, speed=speed, mvacc=mvacc, wait=wait, is_radian=False)

        ###approach the object
        self.approach(**approachDirn,speed=speed, mvacc=mvacc, wait=wait)

        return armHandle.get_position(is_radian=False)[1]

    def verticalPlace(self, objEndPos, approachDirn,
                      gripHoldValue=600,
                      speed=None, mvacc=None, wait=None):

        """
        assumes already holding an object
        
        @params:
        objEndPos = [x...,yaw...] eact obj location
        """
        armHandle = self._armHandle
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)

        ##go to end position
        
        self._currentAttitude = [-180, 0, 0]
        objEndPos[3:] = self._currentAttitude
        
        objEndPos[0] = objEndPos[0] - approachDirn.get('x',0) 
        objEndPos[1] = objEndPos[1] - approachDirn.get('y',0) 
        objEndPos[2] = objEndPos[2] - approachDirn.get('z',0) 
        armHandle.set_position(*objEndPos, speed=speed, mvacc=mvacc, wait=wait, is_radian=False)

        ###approach the table
        self.approach(**approachDirn,speed=speed, mvacc=mvacc, wait=wait)

        ###place the object
        self.holdObject(gripHoldValue,wait = wait)

        ###go back by approach and stand by there
        reverseApproachAfterStart = {key: -value for key, value in approachDirn.items()}
        self.approach(**reverseApproachAfterStart,speed=speed, mvacc=mvacc, wait=wait)

        return armHandle.get_position(is_radian=False)[1]

    def traverseWithPrevAttitude(self, endPosOnlyList,
                                 speed=None, mvacc=None, wait=None):

        """
        Traverse to the new location continuing present attitude
        @ params:
            endPosOnlyList : [x,y,z]



        """
        armHandle = self._armHandle
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        
#        prevAttitutde = armHandle.get_position(is_radian=False)[1][3:]
        prevAttitutde = self._currentAttitude
        
        armHandle.set_position(*endPosOnlyList, *prevAttitutde,
                               speed=speed, mvacc=mvacc, wait=wait, is_radian=False)

        return armHandle.get_position(is_radian=False)[1]

    def approach(self,speed=None,mvacc = None,wait = None, **kwargs):

        """
        @params:
            kwargs = {x:+100,y:-100,....}

        reaches a initial positin near the object and then travels relative
        in the direction of approach to grab the object


        @return :
        """
        ## TODO: make kwargs and delete for wait

        armHandle = self._armHandle

        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)

        armHandle.set_position(**kwargs, relative=True, speed=speed, mvacc=mvacc, wait=wait)

        return armHandle.get_position(is_radian=False)[1]

    def _syncArmsBeforeGripperActions(self,posnOfSelfArm,otherArmHandle= None,posnOfOtherArm= None):
        
        
        """
        need to supply both posnOfOtherArm and OtherArmHandle when syncing both arms
        @params:
            posnOfSelfArm: self Objects position just before the gripper actions
            posnOfOtherArm: other arms position just before the gripper actions
            otherArmHandle: 'arm' of other bot to sync with
            
            
        """
        
        ## first arm waiting
        firstHandle = self._armHandle
        firstHandle.set_position(*posnOfSelfArm,wait=True, is_radian=False)
        
        
        ## second arm waiting
        if posnOfOtherArm is not None and otherArmHandle is not None:
            
            otherArmHandle.set_position(*posnOfOtherArm,wait=True, is_radian=False)
        
        
        return True
    
    
    def syncGripperActions(self,posnOfSelfArm,gripperPosnOfSelfArm, ## self gets the frist ArmHandle
                           otherArmHandle = None,posnOfOtherArm = None,gripperPosnOfOtherArm = None):
        
        
        
        ##syncs robot positions before gripper actions
        self._syncArmsBeforeGripperActions(posnOfSelfArm,otherArmHandle,posnOfOtherArm)
        
        if gripperPosnOfOtherArm is not None and otherArmHandle is not None:
            
            otherArmHandle.set_gripper_position(gripperPosnOfOtherArm, wait=False)
            print("2")
        
        print("Syncing actions")
        firstHandle = self._armHandle
        firstHandle.set_gripper_position(gripperPosnOfSelfArm, wait=True)
        
        print("1")
        ## second arm waiting
        
        
        return True
        
        

if __name__ == '__main__':
    myAct = mainActions('hello')
    #    myAct.approach(x=200)
    myAct._getDefaults(speed=200, mvacc=100, wait=True)




