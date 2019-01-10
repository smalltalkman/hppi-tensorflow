
from __future__ import print_function

import argparse, math
import hppi

def compare_dataset(dataset1_path, dataset2_path):
  print("dataset1: ", dataset1_path)
  print("dataset2: ", dataset2_path)
  dataset1 = hppi.read_data_sets(dataset1_path)
  dataset2 = hppi.read_data_sets(dataset2_path)
  datas1 = dataset1.datas
  datas2 = dataset2.datas
  is_equal = (datas1==datas2)
  not_equal_locations = [(row, column) for row, x in enumerate(is_equal) for column, y in enumerate(x) if not y]
  max_diff = 0
  print("not_equal_locations:")
  for row, column in not_equal_locations:
    print("%6s,%6s: %s,%s"%(row, column, datas1[row][column], datas2[row][column]))
    max_diff = max(max_diff, math.fabs(datas1[row][column]-datas2[row][column]))
  print("max_diff: ", max_diff)

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--input1", help="ppi dataset1 path", required=True)
  parser.add_argument("-b", "--input2", help="ppi dataset2 path", required=True)
  args = parser.parse_args()
  return args

def main():
  args = get_args()
  compare_dataset(args.input1, args.input2)

if __name__=="__main__":
  main()
