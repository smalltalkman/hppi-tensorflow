
import os
import pandas
from Bio import SeqIO
import re
import argparse

def get_args():
  """Parse command line."""
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input",  help="input directory",  required=True)
  parser.add_argument("-o", "--output", help="output directory", required=True)
  args = parser.parse_args()
  return args

def load_irgsp(input_dir, output_dir):
  source = input_dir +"Oryza_sativa.IRGSP-1.0.pep.all.fa"
  target = output_dir+"IRGSP.csv"
  if os.path.exists(target) and os.stat(target).st_mtime>=os.stat(source).st_mtime:
    df = pandas.read_csv(target)
    return df
  df = pandas.DataFrame(columns=('id', 'gene', 'seq'))
  for record in SeqIO.parse(source, "fasta"):
    if record.description:
      gene = re.findall( 'gene:([^ ]+)', record.description )
      if gene:
        df.loc[df.shape[0]] = [ record.id, gene[0], str(record.seq) ]
    # break
  # print(df)
  df.to_csv(target, index=False)
  return df

def load_rap_msu(input_dir, output_dir):
  source = input_dir +"RAP-MSU_2017-08-04.txt"
  target = output_dir+"RAP-MSU.csv"
  if os.path.exists(target) and os.stat(target).st_mtime>=os.stat(source).st_mtime:
    df = pandas.read_csv(target)
    return df
  rap_msu = pandas.read_csv(source, sep='\t', header=None)
  rap_msu = rap_msu[rap_msu[0]!='None']
  rap_msu = rap_msu[rap_msu[1]!='None']
  rap_msu[2] = rap_msu[1].map(lambda s:s.split(',')[0][4:-2])
  # rap_msu = rap_msu[0:5]
  # print(rap_msu)
  new_rap_msu = pandas.DataFrame({'RAP_ID':rap_msu[0], 'MSU_ID':rap_msu[2]})
  # new_rap_msu = new_rap_msu[0:5]
  # print(new_rap_msu)
  new_rap_msu.to_csv(target, index=False)
  return new_rap_msu

def load_ding_xls(input_dir):
  source = input_dir+"Ding-378-Table_S2.xls"
  ding_xls = pandas.read_excel(source, header=2, usecols=[1, 10])[0:-2]
  empty_rows = []
  for index, row in ding_xls.iterrows():
    if row["ID"]==row["ID"]: # is not NaN
      last_row_id = row["ID"]
    elif row["ID.1"]==row["ID.1"]: # is not NaN
      row["ID"] = last_row_id
    else:
      empty_rows.append(index)
  ding_xls.drop(empty_rows, inplace=True)
  # print(ding_xls)
  # ding_xls.to_excel('Ding-378.xls', sheet_name='Sheet1', index=False, header=True)
  return ding_xls

def create_ding_rap(ding_378, rap_msu):
  # ding_378 = pandas.read_excel('Ding-378.xls')
  # print(ding_378)
  # rap_msu = pandas.read_csv('RAP-MSU.csv')
  # print(rap_msu)
  result = ding_378
  result = pandas.merge(result, rap_msu, right_on='MSU_ID', left_on='ID')
  result = pandas.merge(result, rap_msu, right_on='MSU_ID', left_on='ID.1')
  result = result[['RAP_ID_x','RAP_ID_y']]
  # print(result)
  # result.to_csv('Ding-378-RAP.csv', index=False)
  return result

def create_ding(ding_378_rap, irgsp):
  # ding_378_rap = pandas.read_csv('Ding-378-RAP.csv')
  # print(ding_378_rap)
  # irgsp = pandas.read_csv('IRGSP.csv')
  # print(irgsp)
  result = ding_378_rap
  result = pandas.merge(result, irgsp, right_on='gene', left_on='RAP_ID_x')
  result = pandas.merge(result, irgsp, right_on='gene', left_on='RAP_ID_y')
  result = result[['seq_x','seq_y']]
  result = result.drop_duplicates()
  # print(result)
  # result.to_csv('Ding.csv', index=False)
  return result

def load_prin_xls(input_dir):
  source = input_dir+"PRIN_V1.0_rice_experimental_determined_interactions.xls"
  prin_xls = pandas.read_excel(source, usecols=[0, 1])
  # print(prin_xls)
  prin_xls['protein_a_short'] = prin_xls['protein_a'].str[4:]
  prin_xls['protein_b_short'] = prin_xls['protein_b'].str[4:]
  # print(prin_xls)
  result = prin_xls[['protein_a_short','protein_b_short']]
  # print(result)
  result = result.drop_duplicates()
  # print(result)
  # result.to_csv('PRIN_V1.0_rice_experimental_determined_interactions.csv', index=False)
  return result

def create_prin_rap(prin_rice_experimental, rap_msu):
  # prin_rice_experimental = pandas.read_csv('PRIN_V1.0_rice_experimental_determined_interactions.csv')
  # print(prin_rice_experimental)
  # rap_msu = pandas.read_csv('RAP-MSU.csv')
  # print(rap_msu)
  result = prin_rice_experimental
  result = pandas.merge(result, rap_msu, right_on='MSU_ID', left_on='protein_a_short')
  result = pandas.merge(result, rap_msu, right_on='MSU_ID', left_on='protein_b_short')
  result = result[['RAP_ID_x','RAP_ID_y']]
  # print(result)
  result = result.drop_duplicates()
  # result.to_csv('PRIN_V1.0_rice_experimental_determined_interactions-RAP.csv', index=False)
  return result

def create_prin(prin_rice_experimental_rap, irgsp):
  # prin_rice_experimental_rap = pandas.read_csv('PRIN_V1.0_rice_experimental_determined_interactions-RAP.csv')
  # print(prin_rice_experimental_rap)
  # irgsp = pandas.read_csv('IRGSP.csv')
  # print(irgsp)
  result = prin_rice_experimental_rap
  result = pandas.merge(result, irgsp, right_on='gene', left_on='RAP_ID_x')
  result = pandas.merge(result, irgsp, right_on='gene', left_on='RAP_ID_y')
  result = result[['seq_x','seq_y']]
  result = result.drop_duplicates()
  # print(result)
  # result.to_csv('PRIN.csv', index=False)
  return result

def create_positive_protein_pairs(ding, prin, output_dir):
  result = pandas.DataFrame(columns=('seq_x', 'seq_y'))
  result = pandas.concat([result, ding])
  result = pandas.concat([result, prin])
  # print(result)
  result = result.drop_duplicates()
  # print(result)
  result['seq_x'].to_csv(output_dir+'Positive_protein_A.txt', index=False, header=False)
  result['seq_y'].to_csv(output_dir+'Positive_protein_B.txt', index=False, header=False)

def load_uniprot_rap(output_dir):
  df = pandas.read_csv(output_dir+'Subcellular-localization-RAP.csv')
  result = df
  # print(result)
  return result

def load_uniprot(uniprot_rap, irgsp):
  result = uniprot_rap
  result = pandas.merge(result, irgsp, right_on='gene', left_on='rap_id_x')
  result = pandas.merge(result, irgsp, right_on='gene', left_on='rap_id_y')
  result = result[['seq_x','seq_y']]
  result = result.drop_duplicates()
  # print(result)
  # result.to_csv('uniprot.csv', index=False)
  return result

def create_negative_protein_pairs(uniprot, output_dir):
  uniprot['seq_x'].to_csv(output_dir+'Negative_protein_A.txt', index=False, header=False)
  uniprot['seq_y'].to_csv(output_dir+'Negative_protein_B.txt', index=False, header=False)

if __name__=="__main__":
  args = get_args()
  input_dir  = args.input  if args.input .endswith("/") else (args.input +"/")
  output_dir = args.output if args.output.endswith("/") else (args.output+"/")

  irgsp = load_irgsp(input_dir, output_dir)

  rap_msu = load_rap_msu(input_dir, output_dir)
  ding_378 = load_ding_xls(input_dir)
  ding_378_rap = create_ding_rap(ding_378, rap_msu)
  ding_378 = create_ding(ding_378_rap, irgsp)
  prin_xls = load_prin_xls(input_dir)
  prin_rap = create_prin_rap(prin_xls, rap_msu)
  prin = create_prin(prin_rap, irgsp)
  create_positive_protein_pairs(ding_378, prin, output_dir)

  uniprot_rap = load_uniprot_rap(output_dir)
  uniprot = load_uniprot(uniprot_rap, irgsp)
  create_negative_protein_pairs(uniprot, output_dir)
