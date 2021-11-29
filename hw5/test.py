
import sys
import io
##import argparse
import numpy as np
from BitVector import *
import x931

from time import time


if __name__ == '__main__':
    v0 = BitVector(textstring="computersecurity")
    dt = BitVector(intVal=99, size=128)
    listX931 = x931.x931(v0,dt,3,"keyX931.txt")
    #Check if list is correct
    print("{}\n{}\n{}".format(int(listX931[0]),int(listX931[1]),int(listX931[2])))
