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
        self._datas = \
            self.datas_data_file.row(0, self.datas_data_file.rows)
        self.labels_file_name = labels_file_name
        self.labels_data_file = DataFile(file_path, labels_file_name)
        self._labels = \
            self.labels_data_file.row(0, self.labels_data_file.rows)
        if self.datas_data_file.rows > self.labels_data_file.rows:
            self.length = self.labels_data_file.rows
        else:
            self.length = self.datas_data_file.rows
        self.batch_index = 0
        self._epochs_completed = 0
    @property
    def datas(self):
        return self._datas
    @property
    def labels(self):
        return self._labels
    def next_batch(self, length, shuffle=True):
        start = self.batch_index
        if self._epochs_completed == 0 and start == 0 and shuffle:
            perm0 = arange(self.length)
            random.shuffle(perm0)
            self._datas  = self.datas [perm0]
            self._labels = self.labels[perm0]
        if start + length > self.length:
            self._epochs_completed += 1
            rest_num_datas = self.length - start
            datas_rest_part  = self._datas [start:self.length]
            labels_rest_part = self._labels[start:self.length]
            if shuffle:
                perm = arange(self.length)
                random.shuffle(perm)
                self._datas  = self.datas [perm]
                self._labels = self.labels[perm]
            start = 0
            self.batch_index = length - rest_num_datas
            end = self.batch_index
            datas_new_part  = self._datas [start:end]
            labels_new_part = self._labels[start:end]
            return concatenate((datas_rest_part, datas_new_part), axis=0) , concatenate((labels_rest_part, labels_new_part), axis=0)
        else:
            self.batch_index = self.batch_index + length
            end = self.batch_index
            return self._datas[start:end] , self._labels[start:end]

class DataSets:
    def __init__(self, file_path):
        self.file_path = file_path
        self.train = DataSet(file_path, "hppids-train-ppis.bin", "hppids-train-labels.bin")
        self.test  = DataSet(file_path, "hppids-test-ppis.bin",  "hppids-test-labels.bin" )

def read_data_sets(file_path):
    return DataSets(file_path)
