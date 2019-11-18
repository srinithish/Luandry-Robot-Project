# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:03:59 2019

@author: GELab
"""

import pyrealsense2 as rs
import numpy as np
import cv2
import os
import cv2
import colourTracking
import matplotlib.pyplot as plt
import time
import pickle as pk
class DepthCamera():
    
    
    def __init__(self):
        
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)        

        self.pipe_profile = self.pipeline.start(self.config)
        
        
        
        
    def getRGBAndDepthFrame(self):
        
        
        frames = self.pipeline.wait_for_frames()
        newDepthFrame = frames.get_depth_frame()
        newColourFrame = frames.get_color_frame()
        
        
        if not newDepthFrame or not newColourFrame:
            return False
        
        
        self.curr_depth_frame = newDepthFrame
        self.curr_color_frame = newColourFrame
        # Convert images to numpy arrays
        depth_image = np.asanyarray(self.curr_depth_frame.get_data())
        color_image = np.asanyarray(self.curr_color_frame.get_data())
        
        
        return color_image,depth_image
    
    
    def getXYZAtPt(self,PixelX,PixelY):
        
        depth_intrin = self.curr_depth_frame.profile.as_video_stream_profile().intrinsics
        color_intrin = self.curr_color_frame.profile.as_video_stream_profile().intrinsics
        depth_to_color_extrin = self.curr_depth_frame.profile.get_extrinsics_to(
            self.curr_color_frame.profile)
        
        depth = self.curr_depth_frame.get_distance(PixelX, PixelY)
        depth_point = rs.rs2_deproject_pixel_to_point(
                                depth_intrin, [PixelX, PixelY], depth)
        
        
        depth_point = np.array(depth_point)*1000
        
        return depth_point
    
    def stopAndRelease(self):
        self.pipeline.stop()
# Configure depth and color streams
    def transformToRobot1Coords(self,x,y):
        
        
        return 606-x,y+25 
        
    def transformToRobot2Coords(self,x,y):
        
        pass

# Start streaming

if __name__ == '__main__':
    
        
    myCam = DepthCamera()
    counter = 0
    cordList = []
    
    
    while True:
        colorImage,depthImage = myCam.getRGBAndDepthFrame()
#        myCam.getXYZAtPt(200,300)  
        centers,newColorImage = colourTracking.getCenterOfGripper(colorImage)
        
        realWorldCords = myCam.getXYZAtPt(centers[0],centers[1])
        grayDepth = 255*(depthImage - np.min(depthImage))/np.ptp(depthImage).astype(int)
        cordList.append(realWorldCords)
        
        
        if counter % 30 == 0:
            counter = 0
            print(np.mean(cordList, axis = 0))
            cordList = []
            
            
        if cv2.waitKey(1) == 32:
            
            cv2.imwrite("./Data/Keypointdetection/"+str(int(time.time()))+".png",colorImage)
            print("Captured") 
        cv2.imshow("Tracking", newColorImage)
        time.sleep(0.025)
    cv2.destroyAllWindows()
    
    bgArray = pk.load(open('Background.pkl','rb'))
    diffArray = depthImage-bgArray
    plt.matshow(diffArray)
#    pk.dump(depthImage,open('Background.pkl','wb'))
#    plt.imshow(plt.imread("./Data/Keypointdetection/cropped/1573847097.png"))
##    plt.imshow(cv2.cvtColor(colorImage, cv2.COLOR_BGR2RGB))
