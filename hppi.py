'''Load hppi train/test datas and labels
'''

__all__ = ['read_data_sets']

import struct
from numpy import *

class DataFile:
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.file = "%s/%s" % (self.file_path, self.file_name)
        self.head_len = 8
        self.head_fmt = 'ii'
        with open(self.file, 'rb') as file:
            (self.rows, self.columns) = struct.unpack(self.head_fmt, file.read(self.head_len))
        self.item_len = 4
        self.item_fmt = "%if"
    def data_len(self, row_count=1):
        return row_count * self.columns * self.item_len
    def data_fmt(self, row_count=1):
        return self.item_fmt % (row_count * self.columns)
    def data_index(self, index=0):
        return self.head_len + self.data_len(index)
    def row(self, row_start=0, row_count=1):
        with open(self.file, 'rb') as file:
            file.seek(self.data_index(row_start))
            # datas = struct.unpack(self.data_fmt(row_count), file.read(self.data_len(row_count)))
            buf = file.read(self.data_len(row_count))
        # return array(datas, dtype=float32).reshape(row_count, self.columns)
        data = frombuffer(buf, dtype=float32)
        data = data.reshape(row_count, self.columns)
        return data

class DataSet:
    def __init__(self, file_path, datas_file_name, labels_file_name):
        self.file_path = file_path
        self.datas_file_name = datas_file_name
        self.datas_data_file = DataFile(file_path, datas_file_name)
        self.labels_file_name = labels_file_name
        self.labels_data_file = DataFile(file_path, labels_file_name)
        if self.datas_data_file.rows > self.labels_data_file.rows:
            self.length = self.labels_data_file.rows
        else:
            self.length = self.datas_data_file.rows
        self.batch_index = 0
    @property
    def datas(self):
        return self.datas_data_file.row(0, self.datas_data_file.rows)
    @property
    def labels(self):
        return self.labels_data_file.row(0, self.labels_data_file.rows)
    def next_batch(self, length):
        if self.batch_index + length > self.length:
            self.batch_index = 0
        datas = (self. datas_data_file.row(self.batch_index, length),
                 self.labels_data_file.row(self.batch_index, length),
                 )
        self.batch_index = self.batch_index + length
        return datas

class DataSets:
    def __init__(self, file_path):
        self.file_path = file_path
        self.train = DataSet(file_path, "hppids-train-ppis.bin", "hppids-train-labels.bin")
        self.test  = DataSet(file_path, "hppids-test-ppis.bin",  "hppids-test-labels.bin" )

def read_data_sets(file_path):
    return DataSets(file_path)
