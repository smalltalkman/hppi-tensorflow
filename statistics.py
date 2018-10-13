
import argparse

def get_args():
  """Parse command line."""
  parser = argparse.ArgumentParser()
  parser.add_argument("--input",  help="input txt file",  required=True)
  parser.add_argument("--output", help="output csv file", required=True)
  args = parser.parse_args()
  return args

def statistics(INPUT_FILE, OUTPUT_FILE):
    # collect values
    values=[]
    with open(INPUT_FILE, 'r') as input_file:
        line = input_file.readline()
        while line:
            pairs = line.strip().split(',')
            if len(pairs)>=2:
                values.append(pairs[0])
                values.append(pairs[1])
            line = input_file.readline()
    # unique
    values=list(set(values))
    # statistics
    statistics_data={}
    for index, value in enumerate(values):
        size=len(value)
        if not statistics_data.has_key(size):
            statistics_data[size]=1
        else:
            statistics_data[size]=statistics_data[size]+1
    # write to output_file
    with open(OUTPUT_FILE, 'w') as output_file:
        for size, count in statistics_data.items():
            line=str(size)+','+str(count)
            output_file.write(line+'\n')

if __name__=="__main__":
    """main."""
    args = get_args()
    
    statistics(args.input, args.output)
