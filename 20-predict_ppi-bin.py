import sys, os, struct
sys.path.append(os.getcwd())
from coding import *

def generate_flat_file(A_FILE, B_FILE, OUTPUT_FILE):
    lines = 0
    a_file      = open(A_FILE)
    b_file      = open(B_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    print("Generating {0} ...".format(OUTPUT_FILE))
    index = 1
    a_line = a_file.readline()
    b_line = b_file.readline()
    while a_line and b_line:
        if index%2==0:
            a_line=a_line.strip()
            b_line=b_line.strip()
            if len(a_line)>=50 and len(b_line)>=50 :
                output_line = a_line+','+b_line+'\n'
                valid = True
                valid = valid and output_line.find("B")<0
                valid = valid and output_line.find("J")<0
                valid = valid and output_line.find("O")<0
                valid = valid and output_line.find("U")<0
                valid = valid and output_line.find("X")<0
                valid = valid and output_line.find("Z")<0
                if valid:
                    output_file.write(output_line)
                    lines = lines + 1
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        a_line = a_file.readline()
        b_line = b_file.readline()
    print("Generated {0} !".format(OUTPUT_FILE))
    a_file.close()
    b_file.close()
    output_file.close()
    return lines

def numbers_to_str(NUMBERS):
    return ' '.join([str(NUMBER) for NUMBER in NUMBERS])

def generate_ct_file(INPUT_FILE, OUTPUT_FILE):
    lines = 0
    input_file  = open(INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    print("Generating {0} ...".format(OUTPUT_FILE))
    index = 1
    line  = input_file.readline()
    while line:
        line=line.strip()
        if line:
            pairs = line.split(',')
            result = numbers_to_str(ct_code_of(pairs[0])+ct_code_of(pairs[1]))
            output_file.write(result+'\n')
            lines = lines + 1
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line  = input_file.readline()
    print("Generated {0} !".format(OUTPUT_FILE))
    input_file.close()
    output_file.close()
    return lines

def generate_ac_file(INPUT_FILE, OUTPUT_FILE):
    lines = 0
    input_file  = open(INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    print("Generating {0} ...".format(OUTPUT_FILE))
    index = 1
    line = input_file.readline()
    while line:
        line=line.strip()
        if line:
            pairs = line.split(',')
            result = numbers_to_str(ac_code_of(pairs[0])+ac_code_of(pairs[1]))
            output_file.write(result+'\n')
            lines = lines + 1
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = input_file.readline()
    print("Generated {0} !".format(OUTPUT_FILE))
    input_file.close()
    output_file.close()
    return lines

def concat_data_to_file(A_INPUT_FILE, B_INPUT_FILE, OUTPUT_FILE):
    lines = 0
    a_input_file = open(A_INPUT_FILE)
    b_input_file = open(B_INPUT_FILE)
    output_file  = open(OUTPUT_FILE, 'w')
    print("Generating {0} ...".format(OUTPUT_FILE))
    index = 1
    a_line = a_input_file.readline()
    b_line = b_input_file.readline()
    while a_line and b_line:
        a_line=a_line.strip()
        b_line=b_line.strip()
        if a_line and b_line:
            output_line = a_line + " " + b_line + '\n'
            output_file.write(output_line)
            lines = lines + 1
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        a_line = a_input_file.readline()
        b_line = b_input_file.readline()
    print("Generated {0} !".format(OUTPUT_FILE))
    a_input_file.close()
    b_input_file.close()
    output_file.close()
    return lines

def split_data_to_file(dir, pos_file_name, pos_label, pos_max_train_index
                          , neg_file_name, neg_label, neg_max_train_index):
    train_lines = 0
    test_lines  = 0

    hppids_train_ppis   = open(dir+"/hppids-train-ppis.txt"  , 'w')
    hppids_train_labels = open(dir+"/hppids-train-labels.txt", 'w')
    hppids_test_ppis    = open(dir+"/hppids-test-ppis.txt"   , 'w')
    hppids_test_labels  = open(dir+"/hppids-test-labels.txt" , 'w')

    pos_file = "{0}/{1}".format(dir, pos_file_name)
    print("Split {0} ...".format(pos_file))
    positive_interaction_file = open(pos_file)
    index = 1
    line = positive_interaction_file.readline()
    while line:
        line=line.strip()
        if line:
            if index<=pos_max_train_index:
                hppids_train_ppis.write(line+'\n')
                hppids_train_labels.write(pos_label+'\n')
                train_lines = train_lines + 1
            else:
                hppids_test_ppis.write(line+'\n')
                hppids_test_labels.write(pos_label+'\n')
                test_lines = test_lines + 1
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = positive_interaction_file.readline()
    positive_interaction_file.close()

    neg_file = "{0}/{1}".format(dir, neg_file_name)
    print("Split {0} ...".format(neg_file))
    negative_interaction_file = open(neg_file)
    index = 1
    line = negative_interaction_file.readline()
    while line:
        line=line.strip()
        if line:
            if index<=neg_max_train_index:
                hppids_train_ppis.write(line+'\n')
                hppids_train_labels.write(neg_label+'\n')
                train_lines = train_lines + 1
            else:
                hppids_test_ppis.write(line+'\n')
                hppids_test_labels.write(neg_label+'\n')
                test_lines = test_lines + 1
        if index%1000 == 0:
            print("finish index==" + str(index//1000))
        index = index + 1
        line = negative_interaction_file.readline()
    negative_interaction_file.close()

    hppids_train_ppis.close()
    hppids_train_labels.close()
    hppids_test_ppis.close()
    hppids_test_labels.close()

    return (train_lines, test_lines)

def convert_txt_to_bin(txt_file_name, bin_file_name, rows, columns, type, fmt):
    txt_file = open(txt_file_name)
    bin_file = open(bin_file_name, 'wb')
    print("Converting "+txt_file_name+" to "+bin_file_name+" ...")
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

def convert_all_txt_to_bin(dir
                          , train_rows, test_rows
                          , ppi_dims, label_dims
                          , ppi_type, label_type
                          , ppi_fmt , label_fmt
                          ):
    convert_txt_to_bin(dir+"/hppids-train-ppis.txt",   dir+"/hppids-train-ppis.bin",   train_rows,   ppi_dims,   ppi_type,   ppi_fmt)
    convert_txt_to_bin(dir+"/hppids-train-labels.txt", dir+"/hppids-train-labels.bin", train_rows, label_dims, label_type, label_fmt)
    convert_txt_to_bin(dir+"/hppids-test-ppis.txt",    dir+"/hppids-test-ppis.bin",     test_rows,   ppi_dims,   ppi_type,   ppi_fmt)
    convert_txt_to_bin(dir+"/hppids-test-labels.txt",  dir+"/hppids-test-labels.bin",   test_rows, label_dims, label_type, label_fmt)

def main():
    cwd = os.getcwd()
    infos = [("/data/predict_PPI/C.elegan", 3627)
            ,("/data/predict_PPI/Drosophila", 19777)
            ,("/data/predict_PPI/E.coli", 6258)
            ,("/data/predict_PPI/Human", 33318)
            ,("/data/predict_PPI/Yeast", 5348)
            ]
    for dir, max_train_index in infos:
        source_dir = cwd+dir
        # flat
        target_dir = source_dir+"/bin"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        generate_flat_file(source_dir+"/Negative_protein_A.txt"
                          ,source_dir+"/Negative_protein_B.txt"
                          ,target_dir+"/Negative_protein.txt"
                          )
        generate_flat_file(source_dir+"/Positive_protein_A.txt"
                          ,source_dir+"/Positive_protein_B.txt"
                          ,target_dir+"/Positive_protein.txt"
                          )
        # ct
        ct_dir = target_dir+"/ct"
        if not os.path.exists(ct_dir):
            os.makedirs(ct_dir)
        generate_ct_file(target_dir+"/Negative_protein.txt", ct_dir+"/Negative_protein.txt")
        generate_ct_file(target_dir+"/Positive_protein.txt", ct_dir+"/Positive_protein.txt")
        train_lines, test_lines = split_data_to_file(ct_dir, "Positive_protein.txt", "1", max_train_index, "Negative_protein.txt", "0", max_train_index)
        convert_all_txt_to_bin(ct_dir, train_lines, test_lines, 686, 1, float, int, 'f', 'i')
        # ac
        ac_dir = target_dir+"/ac"
        if not os.path.exists(ac_dir):
            os.makedirs(ac_dir)
        generate_ac_file(target_dir+"/Negative_protein.txt", ac_dir+"/Negative_protein.txt")
        generate_ac_file(target_dir+"/Positive_protein.txt", ac_dir+"/Positive_protein.txt")
        train_lines, test_lines = split_data_to_file(ac_dir, "Positive_protein.txt", "1", max_train_index, "Negative_protein.txt", "0", max_train_index)
        convert_all_txt_to_bin(ac_dir, train_lines, test_lines, 420, 1, float, int, 'f', 'i')
        # ct+ac
        ct_ac_dir = target_dir+"/ct+ac"
        if not os.path.exists(ct_ac_dir):
            os.makedirs(ct_ac_dir)
        concat_data_to_file(ct_dir+"/Negative_protein.txt", ac_dir+"/Negative_protein.txt", ct_ac_dir+"/Negative_protein.txt")
        concat_data_to_file(ct_dir+"/Positive_protein.txt", ac_dir+"/Positive_protein.txt", ct_ac_dir+"/Positive_protein.txt")
        train_lines, test_lines = split_data_to_file(ct_ac_dir, "Positive_protein.txt", "1", max_train_index, "Negative_protein.txt", "0", max_train_index)
        convert_all_txt_to_bin(ct_ac_dir, train_lines, test_lines, 1106, 1, float, int, 'f', 'i')

if __name__=="__main__":
    main()
