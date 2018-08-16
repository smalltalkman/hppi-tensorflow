import os, struct

def exclude_empty_line(INPUT_FILE, OUTPUT_FILE):
    input_file = open(INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    index = 1
    line = input_file.readline()
    while line:
        line=line.strip()
        if line:
            output_file.write(line + '\n')
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = input_file.readline()
    input_file.close()
    output_file.close()

def split_data_to_file(dir):
    hppids_train_ppis   = open(dir+"/hppids-train-ppis.txt"  , 'w')
    hppids_train_labels = open(dir+"/hppids-train-labels.txt", 'w')
    hppids_test_ppis    = open(dir+"/hppids-test-ppis.txt"   , 'w')
    hppids_test_labels  = open(dir+"/hppids-test-labels.txt" , 'w')

    print("Split Supp-A-36630-HPRD-positive-interaction.txt ...")
    positive_interaction_file = open(dir+"/Supp-A-36630-HPRD-positive-interaction.txt")
    index = 1
    line = positive_interaction_file.readline()
    while line:
        line=line.strip()
        if line:
            if index<=30000:
                hppids_train_ppis.write(line+'\n')
                hppids_train_labels.write("1"+'\n')
            else:
                hppids_test_ppis.write(line+'\n')
                hppids_test_labels.write("1"+'\n')
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = positive_interaction_file.readline()
    positive_interaction_file.close()

    print("Split Supp-B-36480-HPRD-negative-interaction.txt ...")
    negative_interaction_file = open(dir+"/Supp-B-36480-HPRD-negative-interaction.txt")
    index = 1
    line = negative_interaction_file.readline()
    while line:
        line=line.strip()
        if line:
            if index<=30000:
                hppids_train_ppis.write(line+'\n')
                hppids_train_labels.write("0"+'\n')
            else:
                hppids_test_ppis.write(line+'\n')
                hppids_test_labels.write("0"+'\n')
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = negative_interaction_file.readline()
    negative_interaction_file.close()

    hppids_train_ppis.close()
    hppids_train_labels.close()
    hppids_test_ppis.close()
    hppids_test_labels.close()

def convert_txt_to_bin(txt_file_name, bin_file_name, rows, columns, type, fmt):
    print("Convert "+txt_file_name+" to "+bin_file_name+" ...")
    txt_file = open(txt_file_name)
    bin_file = open(bin_file_name, 'wb')
    bytes = struct.pack('ii', rows, columns)
    bin_file.write(bytes)
    bytes_len = len(bytes)
    index = 1
    line = txt_file.readline()
    while line:
        line=line.strip()
        if line:
            strs = line.split(" ")
            datas = [type(s) for s in strs]
            for data in datas:
                bytes = struct.pack(fmt,data)
                bin_file.write(bytes)
                bytes_len = bytes_len + len(bytes)
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = txt_file.readline()
    print("Converted bytes length= "+str(bytes_len))
    txt_file.close()
    bin_file.close()

def main():
    CWD = os.getcwd()

    ACDD =  CWD + "/data/03-ac"
    ACBDD = CWD + "/data/03-ac-bin"
    if not os.path.exists(ACBDD):
        os.makedirs(ACBDD)

    FILES = [
        "Supp-A-36630-HPRD-positive-interaction.txt",
        "Supp-B-36480-HPRD-negative-interaction.txt",
    ]

    for FILE in FILES:
        print("Processing "+FILE+" ...")
        exclude_empty_line(ACDD+"/"+FILE, ACBDD+"/"+FILE)
        print("Processed!")
    split_data_to_file(ACBDD)
    convert_txt_to_bin(ACBDD+"/hppids-train-ppis.txt",   ACBDD+"/hppids-train-ppis.bin",   60000, 420, float, 'f')
    convert_txt_to_bin(ACBDD+"/hppids-train-labels.txt", ACBDD+"/hppids-train-labels.bin", 60000, 1,     int, 'i')
    convert_txt_to_bin(ACBDD+"/hppids-test-ppis.txt",    ACBDD+"/hppids-test-ppis.bin",    12915, 420, float, 'f')
    convert_txt_to_bin(ACBDD+"/hppids-test-labels.txt",  ACBDD+"/hppids-test-labels.bin",  12915, 1,     int, 'i')
    print("Finished!!!")

if __name__=="__main__":
    main()
