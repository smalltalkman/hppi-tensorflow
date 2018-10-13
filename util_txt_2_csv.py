import os

COLUMNS = [
    'global_step',
    'accuracy',
    'accuracy_baseline',
    'auc',
    'auc_precision_recall',
    'loss',
    'average_loss',
    'label/mean',
    'prediction/mean',
    'train_time',
]

SEPARATOR = ','

def txt_2_csv(INPUT_FILE, OUTPUT_FILE):
    input_file  = open(INPUT_FILE)
    output_file = open(OUTPUT_FILE, 'w')
    index = 1
    line = input_file.readline()
    while line:
        # line=line.strip()
        # print(index, "=", line)
        infos = {}
        pairs = line.split(',')
        for pair in pairs:
            key, value = pair.split('=')
            infos[key.strip()] = value.strip()
        # print(infos)
        if index == 1:
            output_file.write(SEPARATOR.join(COLUMNS)+'\n')
        values = list(map(lambda x:infos[x], COLUMNS))
        output_file.write(SEPARATOR.join(values)+'\n')
        # output_file.write(line+'\n')
        index = index + 1
        line = input_file.readline()
    input_file.close()
    output_file.close()
    pass

def main():
    model_dir = './model'
    if not os.path.exists(model_dir):
        return
    dirs = os.listdir(model_dir)
    for dir in dirs:
        file_path = '{model_dir}/{dir}'.format(model_dir=model_dir, dir=dir)
        # print(file_path)
        tmp_path, tmp_ext = os.path.splitext(file_path)
        if tmp_ext == '.txt':
            new_path = '{file}.csv'.format(file=tmp_path)
            # print(new_path)
            txt_2_csv(file_path, new_path)
    pass

if __name__ == "__main__":
    # main()
    from sys import argv
    _, input, output = argv

    txt_2_csv(input, output)
