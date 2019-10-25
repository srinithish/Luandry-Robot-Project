import os
import sys
import time

from cookingActions import cookingActions
from cookingActions2 import cookingActions2
from mainActions import mainActions
from xarm.wrapper import XArmAPI
from configparser import ConfigParser
import quickNoodlesDemo


quickNoodlesDemo.switchStoveOn()
quickNoodlesDemo.pickGlassAndPour()
quickNoodlesDemo.sprinkleFlavor()
quickNoodlesDemo.sprinkleSalt()
# quickNoodlesDemo.sprinklePepper()
quickNoodlesDemo.sprinkleFlakes()
quickNoodlesDemo.pickAndPlaceNoodles()
quickNoodlesDemo.holdPan()
quickNoodlesDemo.pickStirrerAndStir()
quickNoodlesDemo.releasePan()
quickNoodlesDemo.switchStoveOff()

arm1.disconnect()
arm2.disconnect()

