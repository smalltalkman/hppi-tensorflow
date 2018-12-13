
import os
import pandas
import gzip
from Bio import SeqIO

def export_id_of(uniprot, target_csv):
  # df = pandas.DataFrame(columns=('id', 'original_id', ))
  df = pandas.DataFrame(columns=('id', ))
  with gzip.open(uniprot+".fasta.gz", "rb") as handle:
    for record in SeqIO.parse(handle, "fasta"):
      # df.loc[df.shape[0]] = [ record.id[3:9], record.id, ]
      df.loc[df.shape[0]] = [ record.id[3:9], ]
  df.to_csv(target_csv, index=False, header=False)

prefixs = [ 
'uniprot-20181210-Oryza sativa subsp japonica', 
]

locations = [ 
'cytoplasm', 
'endoplasmic reticulim', 
'golgi apparatus', 
'mitochondrion', 
'nucleus', 
'peroxisome', 
'vacuole', 
]

for prefix in prefixs:
  source_dir = './'+prefix
  target_dir = './'+prefix+'-ids'
  if not os.path.exists(target_dir):
    os.makedirs(target_dir)
  for location in locations:
    export_id_of(source_dir+'/'+prefix+'-'+location, target_dir+'/'+prefix+'-'+location+'.id')
