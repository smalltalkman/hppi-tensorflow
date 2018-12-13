
SOURCE=\
	RAP-MSU_2017-08-04.txt \
	Oryza_sativa.IRGSP-1.0.pep.all.fa \
	Ding-378-Table_S2.xls \
	PRIN_V1.0_rice_experimental_determined_interactions.xls \

.PHONY: default
default: main

.PHONY: uniprot-ids
uniprot-ids:
	python uniprot-export-id.py

Subcellular-localization-RAP.csv: uniprot-export-rap-id.py
	python uniprot-export-rap-id.py

.PHONY: main
main: create_rice_dataset.py $(SOURCE) Subcellular-localization-RAP.csv
	python create_rice_dataset.py
