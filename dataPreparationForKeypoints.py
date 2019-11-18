# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 00:31:53 2019

@author: GELab
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
import cv2




def visualize(normalisedCoordinateArray,imageArray):
    newArray = normalisedCoordinateArray.reshape((-1,2))
    newDenormalised = newArray*imageArray.shape[:-1]
    
    
    dictOfMapping = {0: 'Top Left Collar',
                     1: 'Top Left Shoulder',
                     2: 'Top Left Hand',
                     3: 'Bottom Left Hand',
                     4: 'Corner Left Hand',
                     5: 'Bottom Left Shirt',
                     6: 'Bottom Right Shirt',
                     7: 'Corner Right Hand',
                     8: 'Bottom Right Hand',
                     9: 'Top Right Hand',
                     10: 'Top Right Shoulder',
                     11: 'Top Right Collar'}
    
    
    
    plt.imshow(imageArray)
    for index,pts in enumerate(newDenormalised):
        plt.annotate(dictOfMapping[index],pts)

        
    
    
    pass


def loadToXYArray(imageResizeShape):
    
    labelsDf = pd.read_excel("./Data/Keypointdetection/cropped/labels.xlsx",skiprows = 4,header = None)
    dictOfImagesYAndMask = defaultdict(list)
    
    for index,row in labelsDf.iterrows():
        
        fileName = "./Data/Keypointdetection/cropped/"+str(row[0])+".png"
        imgArray = plt.imread(fileName)
        
        originalShape = imgArray.shape
        CordinatesArray  = row[1:]
        maskArray = np.array((CordinatesArray).astype('int'))
        
        row[1:][row[1:]<0] = 0 ## substiuing by zero for not visible key point
        
        CordinatesArray  = np.array(row[1:])
        
        
        resizedImage = cv2.resize(imgArray,imageResizeShape)
        Normalised_Cooridnates = (CordinatesArray.reshape((-1,2))/imgArray.shape[:-1]).reshape((-1))
        
        dictOfImagesYAndMask['filenames'].append(row[0])
        dictOfImagesYAndMask['imageOriginalShape'].append(originalShape)
        dictOfImagesYAndMask['X_imageArray_original'].append(imgArray)
        dictOfImagesYAndMask['X_imageArray_resized'].append(resizedImage)
        dictOfImagesYAndMask['Masks'].append(maskArray)
        dictOfImagesYAndMask['Coordinates_original'].append(CordinatesArray)
        dictOfImagesYAndMask['Normalised_Cooridnates'].append(Normalised_Cooridnates)
    
    dictOfImagesYAndMask = {key:np.array(value) for key,value in dictOfImagesYAndMask.items()}
    return dictOfImagesYAndMask


if __name__ == "__main__":
        
    myDict = loadToXYArray((400,400))
    visualize(myDict['Normalised_Cooridnates'][0],myDict['X_imageArray_original'][0])
        

