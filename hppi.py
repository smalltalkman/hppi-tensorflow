'''Load hppi train/test datas and labels
'''

__all__ = ['input_data']

import os
from numpy import *

FILES = {
    "train_datas" : "hppids-train-ppis.txt",
    "train_labels": "hppids-train-labels.txt",
    "test_datas"  : "hppids-test-ppis.txt",
    "test_labels" : "hppids-test-labels.txt",
}

def load_datas(dir, key):
    datas = []
    filepath = dir + "/" + FILES[key]
    print("Loading data from " + filepath + " ...")
    file = open(filepath)
    index = 1
    line = file.readline()
    while line:
        line = line.strip()
        if line:
            strs = line.split(" ")
            floats = [float(s) for s in strs]
            datas.append(floats)
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = file.readline()
    file.close()
    return datas

def input_data(dir):
    train_datas  = array(load_datas(dir, "train_datas"),  dtype=float32)
    train_labels = array(load_datas(dir, "train_labels"), dtype=float32)
    test_datas   = array(load_datas(dir, "test_datas"),   dtype=float32)
    test_labels  = array(load_datas(dir, "test_labels"),  dtype=float32)
    datas = {
        "train":{ "datas":train_datas, "labels":train_labels },
        "test" :{ "datas":test_datas,  "labels":test_labels  },
    }
    return datas

if __name__=="__main__":
    dir = os.getcwd() + "/data/09-hppids"
    global hppids
    hppids = input_data(dir)
