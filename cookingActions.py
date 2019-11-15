# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 08:46:47 2019

@author: GELab
"""



from xarm.wrapper import XArmAPI

#import numpy as np

from mainActions import mainActions


class cookingActions(mainActions):
    
    def __init__(self, armHandle, **kwargs):
        
        
        mainActions.__init__(self,armHandle,**kwargs)
#        self._armHandle = armHandle
        # TODO:check for sanity and coonection
        
        pass
    
    
    def setStateAndConnect():
        pass
    
    
    def stir(self,radius,numTimes,speed = None,mvacc=None,wait=None):
        
        
        """
        assumes the TCP is at the center positioned
        
        """
        armHandle = self._armHandle
        
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        circleCenterWithOrient = armHandle.get_position(is_radian=False)[1]
        
        initPosition = list(circleCenterWithOrient)
        initPosition[1]  = initPosition[1] - radius ## change y go up by radius
        
        armHandle.set_position(*initPosition,  is_radian=False,speed=speed, mvacc=mvacc, wait=wait) ## reach the upper point
        
        
        Point2 = list(circleCenterWithOrient)
        Point2[0] = Point2[0]+radius## change x to go right by radius
        
        Point3 = list(circleCenterWithOrient)
        Point3[1] = Point3[1]+radius ##change y to go down by radius
        
        percent = numTimes*100
        ret = armHandle.move_circle(pose1=Point2, pose2=Point3, 
                                    percent=percent, speed=speed, mvacc=mvacc, wait=wait,is_radian=False)
        print('move_circle, ret: {}'.format(ret))
        
        
        
        pass
    
    def makePlusMovement(self,length,numTimes,speed = None,mvacc=None,wait=None):
        armHandle = self._armHandle
        
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        centerPosWithOrient = armHandle.get_position(is_radian=False)[1]
        initPosition = list(centerPosWithOrient)
        ##center
        armHandle.set_position(*initPosition,is_radian=False, speed=speed, mvacc=mvacc, wait=wait) #reach the center point
        
        ## extreme up
        armHandle.set_position(y=length, relative=True, speed=speed, mvacc=mvacc, wait=wait)
        
        
        ## extreme down
        armHandle.set_position(y=-2*length, relative=True, speed=speed, mvacc=mvacc, wait=wait)
        
        ## center again
        armHandle.set_position(*initPosition,is_radian=False, speed=speed, mvacc=mvacc, wait=wait)
        
        
        ## extreme left
        armHandle.set_position(x=-length, relative=True, speed=speed, mvacc=mvacc, wait=wait)
        
        ##extreme right
        armHandle.set_position(x= 2*length, relative=True, speed=speed, mvacc=mvacc, wait=wait)
        
        ## center again
        armHandle.set_position(*initPosition, is_radian=False, speed=speed, mvacc=mvacc, wait=wait)
        
        
        
        pass
        
    
    def flip(self):
        
        
        pass
    
    
    def sprinkle(self,numTimes,tiltBy=45,speed = None,mvacc=None,wait=None):
        
        
        """
        imagines the Tool Orientation is upright
        tiltBy : is the pitch angle
        
        """
        
        
        armHandle = self._armHandle

        
        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        initPosition = armHandle.get_position(is_radian=False)[1]
        # TODO: yet to decide roll or pitch or yaw
        ##position at 45
        armHandle.set_position(*initPosition,speed = speed,mvacc=mvacc, wait=wait,is_radian  = False)
        
        
        
        armHandle.set_position(pitch = -30,speed = speed,mvacc=mvacc, wait=wait,
                               is_radian  = False,relative=True)
        
        
        ### loop here
        for i in range(numTimes):
        ### jerk move front
            armHandle.set_position(x = 50,z = -50,pitch = tiltBy, relative=True,
                                   speed = speed,mvacc=mvacc, wait=wait,is_radian  = False)

            ### jerk move back
            armHandle.set_position(x = -50,z = 50,pitch = -tiltBy,relative=True, 
                                   speed = speed,mvacc=mvacc, wait=wait,is_radian  = False)
            
        
#            ###z motion alone
#            armHandle.set_position(z = -100, relative=True,
#                                   speed = speed,mvacc=mvacc, wait=wait,is_radian  = False)
#
#            ### jerk move back
#            armHandle.set_position(z = 100,relative=True, 
#                                   speed = speed,mvacc=mvacc, wait=wait,is_radian  = False)
         
        ##bring it back to vertical position
        armHandle.set_position(pitch = 30,speed = speed,mvacc=mvacc, wait=wait,
                               is_radian  = False,relative=True)
            
        pass
    
    
    def pour(self, pourDegree,speed = None,mvacc=None,wait=None):
        
        """
        imagines the robot is already at the centerPosWithOrient
        succeeds a pick and place
        
        """
        
        armHandle = self._armHandle
        

        speed, mvacc, wait = self._getDefaults(speed=speed, mvacc=mvacc, wait=wait)
        
        # TODO: yet to decide roll or pitch or yaw
        armHandle.set_position(pitch = pourDegree, relative=True,
                               speed=speed, mvacc =mvacc, wait=wait,is_radian  = False)
        
#        armHandle.set_position(400,0,400,-130,80,0, relative=False, wait=wait,is_radian  = False)
        
        
        ## depour
        armHandle.set_position(pitch = -pourDegree, relative=True, 
                               speed= speed,mvacc= mvacc,wait=wait,is_radian  = False)
        
        
        pass
    

if __name__ == '__main':
    
    
    #test functions here
    pass
        
        
        
        
        
        
        
        