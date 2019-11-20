import os
import sys

ROOT_DIR = os.path.join(os.getcwd(),"Mask_RCNN")
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR,"samples/coco/"))



import cv2
import coco
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage
import glob
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log
import visualize_cv2
import dog


# Root directory of the project

# Import Mask RCNN
  # To find local version of the library

#custom_WEIGHTS_PATH = sorted(glob.glob("/Users/juanhuerta/logs/*/mask_rcnn_*.h5"))[-1]
custom_WEIGHTS_PATH = os.path.join(ROOT_DIR,"logs/balloon20191118T2308/mask_rcnn_balloon_0030.h5")
# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

config = dog.DogConfig()
custom_DIR = os.path.join(ROOT_DIR, "datasets/laundry")


class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
config.display()

# Device to load the neural network on.
# Useful if you're training a model on the same
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/gpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"

# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                              config=config)

# load the last model you trained
# weights_path = model.find_last()[1]

# Load weights
print("Loading weights ", custom_WEIGHTS_PATH)
model.load_weights(custom_WEIGHTS_PATH, by_name=True)

from importlib import reload  # was constantly changin the visualization, so I decided to reload it instead of notebook

reload(visualize)

frame = cv2.VideoCapture(0)


fileList = glob.glob("./Mask_RCNN/datasets/laundry/val/*.png")


for file in fileList:
    image = cv2.imread(file)

    results = model.detect([image], verbose=1)

    r = results[0]

    im = visualize_cv2.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                     ['BG', 'shirt'], r['scores'])
    cv2.waitKey(1)
    
    cv2.imshow('Trackinf',im)

									 
                                                                                                            								