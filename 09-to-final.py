import os

# Current work directory
CWD = os.getcwd()

# CT data directory
CTDD = CWD + "/data/02-ct"
# AC data directory
ACDD = CWD + "/data/03-ac"
# Final data directory
FDD  = CWD + "/data/09-hppids"

# Files
FILES = [
    ("Supp-A-36630-HPRD-positive-interaction.txt", [1, 0]),
    ("Supp-B-36480-HPRD-negative-interaction.txt", [0, 1]),
]

def generate_total_data_file(CT_INPUT_FILE, AC_INPUT_FILE, OUTPUT_FILE):
    ct_input_file = open(CT_INPUT_FILE)
    ac_input_file = open(AC_INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    index = 1
    ct_line = ct_input_file.readline()
    ac_line = ac_input_file.readline()
    while ct_line and ac_line:
        ct_line=ct_line.strip('\n')
        ac_line=ac_line.strip('\n')
        if ct_line and ac_line:
            output_line = ct_line + " " + ac_line + "\n"
            output_file.write(output_line)
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        ct_line = ct_input_file.readline()
        ac_line = ac_input_file.readline()
    ct_input_file.close()
    ac_input_file.close()
    output_file.close()

def split_data_to_file():
    hppids_train_ppis   = open(CWD+"/data/09-hppids/hppids-train-ppis.txt"  , 'w')
    hppids_train_labels = open(CWD+"/data/09-hppids/hppids-train-labels.txt", 'w')
    hppids_test_ppis    = open(CWD+"/data/09-hppids/hppids-test-ppis.txt"   , 'w')
    hppids_test_labels  = open(CWD+"/data/09-hppids/hppids-test-labels.txt" , 'w')

    print("Split Supp-A-36630-HPRD-positive-interaction.txt ...")
    positive_interaction_file = open(CWD+"/data/09-hppids/Supp-A-36630-HPRD-positive-interaction.txt")
    index = 1
    line = positive_interaction_file.readline()
    while line:
        line=line.strip('\n')
        if line:
            if index<=30000:
                hppids_train_ppis.write(line+"\n")
                hppids_train_labels.write("1 0\n")
            else:
                hppids_test_ppis.write(line+"\n")
                hppids_test_labels.write("1 0\n")
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = positive_interaction_file.readline()
    positive_interaction_file.close()

    print("Split Supp-B-36480-HPRD-negative-interaction.txt ...")
    negative_interaction_file = open(CWD+"/data/09-hppids/Supp-B-36480-HPRD-negative-interaction.txt")
    index = 1
    line = negative_interaction_file.readline()
    while line:
        line=line.strip('\n')
        if line:
            if index<=30000:
                hppids_train_ppis.write(line+"\n")
                hppids_train_labels.write("0 1\n")
            else:
                hppids_test_ppis.write(line+"\n")
                hppids_test_labels.write("0 1\n")
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = negative_interaction_file.readline()
    negative_interaction_file.close()

    hppids_train_ppis.close()
    hppids_train_labels.close()
    hppids_test_ppis.close()
    hppids_test_labels.close()

if __name__=="__main__":
    for FILE, _ in FILES:
        print("Processing "+FILE+" ...")
        generate_total_data_file(CTDD+"/"+FILE, ACDD+"/"+FILE, FDD+"/"+FILE)
        print("Processed!")
    split_data_to_file()
    print("Finished!!!")
