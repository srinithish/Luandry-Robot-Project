# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:42:05 2019

@author: nithish
"""



import tensorflow as tf
import numpy as np
import sklearn
import pandas as pd
import dataPreparationForKeypoints
import cv2 as cv2
import time

NCLASSES = 24
tf.test.is_gpu_available()

trainingDict = dataPreparationForKeypoints.loadToXYArray((400,400))

baseModel = tf.keras.applications.inception_resnet_v2.InceptionResNetV2(weights = "imagenet",
                                                                        include_top = False,
                                                    input_shape=(400,400,3))
#model = vgg16.VGG16(weights='imagenet', include_top=False, input_shape=(160,320,3))

layer1 = { "type":"conv2d",
            "filters":16,
            "kernel_size":[4,4],
            "activation": tf.nn.leaky_relu
         }

layer2 = { "type":"maxpool",
            "pool_size":3,
            "padding":'valid'
         }


layer3 = { "type":"conv2d",
            "filters":32,
            "kernel_size":[4,4],
          "activation": tf.nn.leaky_relu
         }

layer4 = { "type":"maxpool",
            "pool_size":3,
            "padding":'valid'
         }



layer5 = { "type":"fullyConnected",
            'outputUnits': NCLASSES,
            
            "activation": tf.nn.leaky_relu
          }

layerStack = [layer1,layer2,layer3,layer4,layer5]


def get_network_output(input_x,layers):
    '''
    
    inputs = baseModelInput
    output = latent_vectors
    
    input.shape => (batch_size,28,28)  // We need to reshape to add filters dim
    output.shape => (batch_size,6)  //6 values corresponding to 3 means and 3 sd
    '''
    constructed_network = []
    
    # He initialization
    initializer = tf.keras.initializers.he_normal()
        
    for layer in layers:
      
        if len(constructed_network) == 0: # This is the First layer
            this_input = input_x
        else:
            this_input = constructed_network[-1]
   
      
        if layer["type"] == "conv2d":
            layerOutput = tf.keras.layers.Conv2D( 
                         
                         filters = layer["filters"],
                         kernel_size = layer["kernel_size"],
                         strides = 1,
                         padding = "same",
                         kernel_initializer = initializer,
                         activation = layer["activation"]
                        )(this_input)
        
        elif layer["type"] == "maxpool":
            layerOutput = tf.keras.layers.MaxPool2D(
                         
                          pool_size = layer["pool_size"],
                          strides = layer["pool_size"], # Same as pool size to not consider the same box twice
                          padding='valid')(this_input)
        
        
        elif layer['type'] == 'fullyConnected':
          
            this_input = tf.keras.layers.Flatten()(this_input) ##flatten input
          
            layerOutput = tf.keras.layers.Dense(
                              units = layer['outputUnits'],
                              activation = layer["activation"],
                              kernel_initializer= initializer)(this_input)

            
        
        # Push this layer to network
        constructed_network.append(layerOutput)
      
    return constructed_network[-1]



topNetWorkOutput = get_network_output(input_x = baseModel.output,layers = layerStack)


###network params

initializer = tf.keras.initializers.he_normal()
optimizer = tf.keras.optimizers.Adam()




XYCoordinatePredictions = tf.keras.layers.Dense(
                              units = 24,
                              activation = tf.nn.sigmoid,
                              kernel_initializer= initializer,name= "XYLayer")(topNetWorkOutput)



maskPredictions = tf.keras.layers.Dense(
                              units = 24,
                              activation = tf.nn.sigmoid,
                              kernel_initializer= initializer,name= "maskLayer")(topNetWorkOutput)




fullModel = tf.keras.Model(inputs= baseModel.input,outputs = [XYCoordinatePredictions,maskPredictions])


for layer in baseModel.layers:
    layer.trainable = False


fullModel.compile(loss = ['mse',"binary_crossentropy"],optimizer = optimizer)
fullModel.summary()
fullModel.fit(x=trainingDict['X_imageArray_resized'],
              y=[trainingDict['Normalised_Cooridnates'],trainingDict['Masks']],
              epochs= 50,validation_split = 0.1)

#### visualize predictions
predictions = fullModel.predict(trainingDict['X_imageArray_resized'])

for index,pred in enumerate(predictions):
    
    dataPreparationForKeypoints.visualize(pred[0],trainingDict['X_imageArray_original'][index])