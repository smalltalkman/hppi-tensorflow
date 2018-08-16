# Append module path.
import sys, os
sys.path.append(os.getcwd())

# Import module
from coding import *

# Current work directory
CWD = os.getcwd()

# Flat data directory
FDD = CWD + "/data/01-flat"
# AC data directory
ACDD = CWD + "/data/03-ac"

# Files
FILES = [
    "Supp-A-36630-HPRD-positive-interaction.txt",
    "Supp-B-36480-HPRD-negative-interaction.txt",
    "Supp-C-3899-HPRD-positive-interaction-below-0.25.txt",
    "Supp-D-4262-HPRD-negative-interaction-below-0.25.txt",
    "Supp-E-1882-interacting-0.5-non-interacting-0.5.txt",
]

def numbers_to_str(NUMBERS):
    return ' '.join([str(NUMBER) for NUMBER in NUMBERS])

def generate_ac_file(INPUT_FILE, OUTPUT_FILE):
    input_file = open(INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    index = 1
    line = input_file.readline()
    while line:
        line=line.strip()
        # print(index, "=", line)
        if line:
            pairs = line.split(',')
            result = numbers_to_str(ac_code_of(pairs[0])+ac_code_of(pairs[1]))
            output_file.write(result+'\n')
        else:
            output_file.write('\n')
        # output_file.write(line+'\n')
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = input_file.readline()
    input_file.close()
    output_file.close()

if __name__=="__main__":
    if not os.path.exists(ACDD):
        os.makedirs(ACDD)
    for FILE in FILES:
        print("Processing "+FILE+" ...")
        generate_ac_file(FDD+"/"+FILE, ACDD+"/"+FILE)
        print("Processed!")
    print("Finished!!!")
