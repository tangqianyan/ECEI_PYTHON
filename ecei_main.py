import codecs
import read_data as rd
import process_data as pd

DIR =r"/home/chixiao/projects/ECEI/"



if __name__ == "__main__":
    data = rd.get_data(DIR,[0,0.0001],0.0001)
    print(data[:,:,-1])
    print(data[:,:,-2])
    pd.show_data(data)
