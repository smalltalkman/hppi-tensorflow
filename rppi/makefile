
SOURCE=\
	resource/Oryza_sativa.IRGSP-1.0.pep.all.fa \
	resource/RAP-MSU_2017-08-04.txt \
	resource/Ding-378-Table_S2.xls \
	resource/PRIN_V1.0_rice_experimental_determined_interactions.xls \
	resource/PRIN_V1.0_rice_predicted_interactions_High_Coverage.txt \

.PHONY: default
default: Rice Rice2

.PHONY: uniprot-ids
uniprot-ids:
	python uniprot-export-id.py

Rice/Subcellular-localization-RAP.csv: uniprot-export-rap-id.py
	python uniprot-export-rap-id.py -n  7 -o "$@"

.PHONY: Rice
Rice: create_rice_dataset.py $(SOURCE) Rice/Subcellular-localization-RAP.csv
	python create_rice_dataset.py -i resource -o Rice

Rice2/Subcellular-localization-RAP.csv: uniprot-export-rap-id.py
	python uniprot-export-rap-id.py -n 50 -o "$@"

.PHONY: Rice2
Rice2: create_rice_dataset.py $(SOURCE) Rice2/Subcellular-localization-RAP.csv
	python create_rice_dataset.py -i resource -o Rice2 --printype high_confidence
