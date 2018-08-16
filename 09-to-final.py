import os, struct

def generate_total_data_file(CT_INPUT_FILE, AC_INPUT_FILE, OUTPUT_FILE):
    ct_input_file = open(CT_INPUT_FILE)
    ac_input_file = open(AC_INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    index = 1
    ct_line = ct_input_file.readline()
    ac_line = ac_input_file.readline()
    while ct_line and ac_line:
        ct_line=ct_line.strip()
        ac_line=ac_line.strip()
        if ct_line and ac_line:
            output_line = ct_line + " " + ac_line + '\n'
            output_file.write(output_line)
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        ct_line = ct_input_file.readline()
        ac_line = ac_input_file.readline()
    ct_input_file.close()
    ac_input_file.close()
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
    # Current work directory
    CWD = os.getcwd()

    # CT data directory
    CTDD = CWD + "/data/02-ct"
    # AC data directory
    ACDD = CWD + "/data/03-ac"
    # Final data directory
    FDD  = CWD + "/data/09-hppids"
    if not os.path.exists(FDD):
        os.makedirs(FDD)

    # Files
    FILES = [
        ("Supp-A-36630-HPRD-positive-interaction.txt", [1, 0]),
        ("Supp-B-36480-HPRD-negative-interaction.txt", [0, 1]),
    ]

    for FILE, _ in FILES:
        print("Processing "+FILE+" ...")
        generate_total_data_file(CTDD+"/"+FILE, ACDD+"/"+FILE, FDD+"/"+FILE)
        print("Processed!")
    split_data_to_file(FDD)
    convert_txt_to_bin(FDD+"/hppids-train-ppis.txt",   FDD+"/hppids-train-ppis.bin",   60000, 1106, float, 'f')
    convert_txt_to_bin(FDD+"/hppids-train-labels.txt", FDD+"/hppids-train-labels.bin", 60000, 1,      int, 'i')
    convert_txt_to_bin(FDD+"/hppids-test-ppis.txt",    FDD+"/hppids-test-ppis.bin",    12915, 1106, float, 'f')
    convert_txt_to_bin(FDD+"/hppids-test-labels.txt",  FDD+"/hppids-test-labels.bin",  12915, 1,      int, 'i')
    print("Finished!!!")

if __name__=="__main__":
    main()
