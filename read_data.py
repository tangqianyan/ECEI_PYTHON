from __future__ import division
import numpy as np
import codecs 
import struct
import math

def scan(shot_dir,Time,Fs=1e6,PRE=0):

    if len(Time) < 2 or Time[0] > Time[1]:
        print ("The Time must be a timeslice and Time[0] <= Time[1] !")

    try:
        fid = open(shot_dir,'r')

        indx1 = int(round(Time[0]*Fs))
        length = int(round((Time[1]-Time[0])*Fs))

        fid.seek((indx1+PRE)*2)
        fmt = str(length)+"h"
        tmp = struct.unpack(fmt, fid.read(length*2))
        tmp = np.array(tmp)/2**15
        return tmp
    except IOError:
        print ("Can't open " + shot_dir + ", Check your directory !")


def CR2IPeast2012(CHANNEL,ROW):
    MIP = [[106,112],[105,111],[104, 110],[109,115],[108,114],[107,113]]

    if ROW % 8 == 0:
        r_Row = 8
    else:
        r_Row = ROW % 8

    if CHANNEL % 4 == 0:
        r_Channel = 4
    else:
        r_Channel = CHANNEL % 4
    IP = MIP[int(math.floor((CHANNEL-1)/4))][int(math.floor((ROW-1)/8))]
    CH = 8*(r_Channel-1) + r_Row

    return (IP,CH)

def loadeceieast1(SHOT,Channel,Row,Time,DIR,Fs=1e6,Default=0):

    if SHOT < 44000:
        [IP,CH] = CR2IPeast2012(Channel,Row)

        # the number of data acquisition before triger
        PRE = 1e5
    else:
        print ("SHOT should <44000")
#    elif SHOT < 60000:
#        [IP,CH] = CR2IPeast2014(Channel,Row)
#        PRE = 83e3
#    else:
#        [IP,CH] = CR2IPeast2015(Channel,Row)

    # set shot directory
    shot_dir = DIR + "SHOT." + str(SHOT).zfill(6) + r"/acq132_" + str(IP) + r"/CH" + str(CH).zfill(2)

    # read data
    tmp = scan(shot_dir,Time,Fs,PRE)

    if PRE != 0:
        tmpPRE = scan(shot_dir,[0,PRE/Fs],Fs,0)

    if Default != 0:
        data = tmp - np.mean(tmpPRE)
    else:
        data = tmp

    return tmp


def read_data(DIR,SHOT,START_END_TIME):

    CH = 24
    ROW = 16
    Fs = 1e6
    length = int(round((START_END_TIME[1]-START_END_TIME[0])*Fs))

    data = np.empty((CH,ROW,length))

    SHOT = int(SHOT)
    #while START_END_TIME[0] < START_END_TIME[1]:
    for i_ch in range(1,CH+1):
        for i_row in range(1,ROW+1):
            data_one = loadeceieast1(SHOT,i_ch,i_row,START_END_TIME,DIR,Fs,1)
            data[i_ch-1,i_row-1,:] = data_one

    #data = np.array(data)
    print (data.shape[2])
    return data


def get_data(DIR,START_END_TIME,DURATION):

    CH =24
    ROW = 16

    with codecs.open('./config/shot_number.txt',"r","utf-8") as fid:
        SHOT_LIST = []
        for line in fid:
            if line == '\n':
                continue
            line = line.strip()
            SHOT_LIST.append(line)

    for SHOT in SHOT_LIST:
        data = read_data(DIR,SHOT,START_END_TIME)

    return data
 
#if __name__ == "__main__":
#    tmp = loadeceieast1(42987,24,16,[0.00,0.0001],r"/home/chixiao/projects/ECEI/",1e6,0)
#    print(tmp)
