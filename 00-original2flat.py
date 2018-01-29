import os

# Current work directory
CWD = os.getcwd()

# Original data directory
ODD = CWD + "/data/00-original"
# Flat data directory
FDD = CWD + "/data/01-flat"

# Files
FILES = [
    ("Supp-A-36630-HPRD-positive-interaction.txt", 0),
    ("Supp-B-36480-HPRD-negative-interaction.txt", 0),
    ("Supp-C-3899-HPRD-positive-interaction-below-0.25.txt", 0),
    ("Supp-D-4262-HPRD-negative-interaction-below-0.25.txt", 1),
    ("Supp-E-1882-interacting-0.5-non-interacting-0.5.txt", -1),
]

def generate_flat_file(INPUT_FILE, OUTPUT_FILE, shift):
    input_file = open(INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    index = 1
    line = input_file.readline()
    while line:
        if (index+shift)>=5 and ( (index+shift)%5==2 or (index+shift)%5==4 ):
            line=line.strip('\n')
            # print(index, "=", line)
            if (index+shift)%5 == 2:
                output_line = line + ','
            elif (index+shift)%5 == 4:
                output_line = output_line + line + '\n'
                valid = True
                valid = valid and output_line.find("B")<0
                valid = valid and output_line.find("J")<0
                valid = valid and output_line.find("O")<0
                valid = valid and output_line.find("U")<0
                valid = valid and output_line.find("X")<0
                valid = valid and output_line.find("Z")<0
                pairs = output_line.strip('\n').split(',')
                valid = valid and len(pairs[0])>=50 and len(pairs[1])>=50
                if valid:
                    output_file.write(output_line)
                else:
                    print("skip index="+str((index+shift)//5))
                    output_file.write('\n')
        index = index + 1
        line = input_file.readline()
    input_file.close()
    output_file.close()

if __name__=="__main__":
    for FILE, SHIFT in FILES:
        print("Processing "+FILE+" ...")
        generate_flat_file(ODD+"/"+FILE, FDD+"/"+FILE, SHIFT)
        print("Processed!")
    print("Finished!!!")
