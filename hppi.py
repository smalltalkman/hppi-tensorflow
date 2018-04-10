'''Load hppi train/test datas and labels
'''

__all__ = ['read_data_sets']

import struct
from numpy import *

def dense_to_one_hot(labels_dense, num_classes):
    num_labels = labels_dense.shape[0]
    index_offset = arange(num_labels) * num_classes
    labels_one_hot = zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
    return labels_one_hot

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
    def row(self, row_start=0, row_count=1, dt=float32, one_hot=False, num_classes=2):
        with open(self.file, 'rb') as file:
            file.seek(self.data_index(row_start))
            # datas = struct.unpack(self.data_fmt(row_count), file.read(self.data_len(row_count)))
            buf = file.read(self.data_len(row_count))
        # return array(datas, dtype=float32).reshape(row_count, self.columns)
        data = frombuffer(buf, dtype=dt)
        if self.columns>=2:
            data = data.reshape(row_count, self.columns)
        elif one_hot:
            data = dense_to_one_hot(data, num_classes)
        return data

class DataSet:
    def __init__(self, file_path, datas_file_name, labels_file_name, one_hot=False, num_classes=2, datas_dt=float32, labels_dt=int32):
        self.file_path = file_path
        self.datas_file_name = datas_file_name
        self.datas_data_file = DataFile(file_path, datas_file_name)
        self._datas = \
            self.datas_data_file.row(0, self.datas_data_file.rows, datas_dt, False)
        self.labels_file_name = labels_file_name
        self.labels_data_file = DataFile(file_path, labels_file_name)
        self._labels = \
            self.labels_data_file.row(0, self.labels_data_file.rows, labels_dt, one_hot, num_classes)
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
    def shuffle(self):
        perm = arange(self.length)
        random.shuffle(perm)
        self._datas  = self.datas [perm]
        self._labels = self.labels[perm]
        return self
    def split(self, ratio=0.75):
        train_length = int(self.length*ratio)
        validation_length = self.length-train_length
        
        train_datas  = self._datas [:train_length]
        train_labels = self._labels[:train_length]
        validation_datas  = self._datas [train_length:]
        validation_labels = self._labels[train_length:]
        
        return train_length, train_datas, train_labels, validation_length, validation_datas, validation_labels

class DataSets:
    def __init__(self, file_path, one_hot=False):
        self.file_path = file_path
        self.train = DataSet(file_path, "hppids-train-ppis.bin", "hppids-train-labels.bin", one_hot)
        self.test  = DataSet(file_path, "hppids-test-ppis.bin",  "hppids-test-labels.bin" , one_hot)
        self._datas  = concatenate((self.train.datas,  self.test.datas ), axis=0)
        self._labels = concatenate((self.train.labels, self.test.labels), axis=0)
        self._datas_length  = self._datas.shape[0]
        self._labels_length = self._labels.shape[0]
        if self._datas_length > self._labels_length:
            self.length = self._labels_length
        else:
            self.length = self._datas_length
    @property
    def datas(self):
        return self._datas
    @property
    def labels(self):
        return self._labels
    def shuffle(self):
        perm = arange(self.length)
        random.shuffle(perm)
        self._datas  = self.datas [perm]
        self._labels = self.labels[perm]
        return self
    def split(self, apply=False):
        train_length = self.train.length
        
        train_datas  = self._datas [:train_length]
        train_labels = self._labels[:train_length]
        test_datas  = self._datas [train_length:]
        test_labels = self._labels[train_length:]
        
        if(apply):
            self.train.length  = train_length
            self.train._datas  = train_datas
            self.train._labels = train_labels
            self.test.length  = self.length - train_length
            self.test._datas  = test_datas
            self.test._labels = test_labels
        
        return train_datas, train_labels, test_datas, test_labels

def read_data_sets(file_path, one_hot=False):
    return DataSets(file_path, one_hot)
