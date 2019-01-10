
import os
import struct
import argparse
import numpy
import pandas
import multiprocessing
from coding import *
import zipfile

code_methods={
   'ct' : ct_code_of,
   'ac' : ac_code_of,
   'ld' : ld_code_of,
  'mos' :mos_code_of,
}

def do_coding(source, code_method):
  coding = lambda x: pandas.Series( code_methods[code_method](x[0]) + code_methods[code_method](x[1]) )
  target = source.apply(coding, axis=1)
  return target

def do_coding_wrapper(args):
  return do_coding(*args)

def parallelize_coding(source, code_method):
  source_split = numpy.array_split(source, multiprocessing.cpu_count())
  pool = multiprocessing.Pool(multiprocessing.cpu_count())
  target = pandas.concat(pool.map(do_coding_wrapper, [(x, code_method) for x in source_split]))
  pool.close()
  pool.join()
  return target

def load_data(csv_file, code_method, label):
  source = pandas.read_csv(csv_file, header=None)
  # source = source[0:5]
  target = parallelize_coding(source, code_method)
  return target, pandas.DataFrame({'label':[label]*target.shape[0]})

def save_data(df, bin_file_name, type, fmt):
  rows, cols = df.shape
  with open(bin_file_name, 'wb') as bin_file:
    bytes = struct.pack('ii', rows, cols)
    bin_file.write(bytes)
    for index, row in df.iterrows():
      datas = [type(v) for v in row.tolist()]
      for data in datas:
        bytes = struct.pack(fmt,data)
        bin_file.write(bytes)

def mkdir(path):
  sub_path = os.path.dirname(path)
  if not os.path.exists(sub_path):
    mkdir(sub_path)
  if not os.path.exists(path):
    os.mkdir(path)

def rmdir(path):
  if os.path.isdir(path):
    for dir in os.listdir(path):
      sub_path = path+'/'+dir
      if os.path.isdir(sub_path):
        rmdir(sub_path)
      else:
        os.remove(sub_path)
    os.rmdir(path)

def do_process(positive_csv, negative_csv, output_dir, code_method, splits):
  positive_ppis, positive_labels = load_data(positive_csv, code_method, 1)
  negative_ppis, negative_labels = load_data(negative_csv, code_method, 0)
  # print(positive_ppis)
  # print(positive_labels)
  # print(negative_ppis)
  # print(negative_labels)
  if len(splits)==0:
    splits.append(0.5)
  if len(splits)==1:
    splits.append(splits[0])
  positive_split = splits[0]
  negative_split = splits[1]
  if positive_split<1.0:
    positive_split *= positive_ppis.shape[0]
  if negative_split<1.0:
    negative_split *= negative_ppis.shape[0]
  positive_split = int(positive_split)
  negative_split = int(negative_split)
  train_ppis   = pandas.concat([ positive_ppis  [:positive_split], negative_ppis  [:negative_split] ])
  train_labels = pandas.concat([ positive_labels[:positive_split], negative_labels[:negative_split] ])
  test_ppis    = pandas.concat([ positive_ppis  [positive_split:], negative_ppis  [negative_split:] ])
  test_labels  = pandas.concat([ positive_labels[positive_split:], negative_labels[negative_split:] ])
  # print(train_ppis)
  # print(train_labels)
  # print(test_ppis)
  # print(test_labels)
  mkdir(output_dir)
  save_data(train_ppis,   output_dir+'/hppids-train-ppis.bin',   float, 'f')
  save_data(train_labels, output_dir+'/hppids-train-labels.bin',   int, 'i')
  save_data(test_ppis,    output_dir+'/hppids-test-ppis.bin',    float, 'f')
  save_data(test_labels,  output_dir+'/hppids-test-labels.bin',    int, 'i')
  # target.to_csv(output_csv, header=False, index=False)
  with zipfile.ZipFile(output_dir+'.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.write(output_dir+'/hppids-train-ppis.bin'  , arcname='hppids-train-ppis.bin'  )
    zip_file.write(output_dir+'/hppids-train-labels.bin', arcname='hppids-train-labels.bin')
    zip_file.write(output_dir+'/hppids-test-ppis.bin'   , arcname='hppids-test-ppis.bin'   )
    zip_file.write(output_dir+'/hppids-test-labels.bin' , arcname='hppids-test-labels.bin' )
  rmdir(output_dir)

def get_args():
  """Parse command line."""
  float_list = lambda x: list(map( float, x.split(";") ))
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--inputP", help="positive interaction file", required=True)
  parser.add_argument("-n", "--inputN", help="negative interaction file", required=True)
  parser.add_argument("-o", "--output", help="output directory", required=True)
  parser.add_argument("-m", "--method", help="coding method", required=True)
  parser.add_argument("-s", "--splits", help="count or ratio of positive items", required=True, type=float_list)
  args = parser.parse_args()
  return args

def main():
  args = get_args()
  do_process(args.inputP, args.inputN, args.output, args.method, args.splits)

if __name__=="__main__":
  main()
