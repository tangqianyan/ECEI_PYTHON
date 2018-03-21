#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: process_data.py
#Author: chi xiao
#Mail: 
#Created Time:
############################

from PIL import Image
from scipy.misc import imsave
import numpy as np


def show_data(data):
    for i in range(data.shape[2]):
        img = data[:,:,i]
        name = 'image_' + str(i) + '.jpg'
        imsave(name,img)
        #print(data[:,:,i])
