from __future__ import division
import numpy as np
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



#if __name__ == "__main__":
#    tmp = loadeceieast1(42987,6,6,[6.00,6.0001],r"/home/chixiao/projects/ECEI/",1e6,0)
#    print(tmp)
