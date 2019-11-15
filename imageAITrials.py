# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 23:02:51 2019

@author: GELab
"""

#from imageai.Detection import ObjectDetection
#import os
#import tensorflow as tf
#tf.__version__
#
#execution_path = os.getcwd()
#
#detector = ObjectDetection()
#detector.setModelTypeAsYOLOv3()
#detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
#detector.loadModel()
#detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "image2.jpg"), output_image_path=os.path.join(execution_path , "image2new.jpg"), minimum_percentage_probability=30)
#
#for eachObject in detections:
#    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
#    print("--------------------------------")
#    
#    
###############

from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="hololens")
trainer.setTrainConfig(object_names_array=["hololens"], batch_size=4, num_experiments=200, train_from_pretrained_model="pretrained-yolov3.h5")
# In the above,when training for detecting multiple objects,
#set object_names_array=["object1", "object2", "object3",..."objectz"]
trainer.trainModel()