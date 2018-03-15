import codecs
import read_data as rd

def process(START_END_TIME,DURATION):

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
        SHOT = int(SHOT)
        DIR =r"/home/chixiao/projects/ECEI/"
        #+r"SHOT." + str(SHOT).zfill(6) + r"/acq132_"
        #+ str(IP) + r"/CH" + str(CH)
        while START_END_TIME[0] < START_END_TIME[1]:
            for i_ch in range(CH):
                for i_row in range(ROW):
                    data_one = rd.loadeceieast1(SHOT,i_ch,i_row,START_END_TIME,DIR,1e6,1)
                    print (data_one)



if __name__ == "__main__":
    process([0,1],0.6)

