
ORIGINAL_DIR=data/00-original
ORIGINAL_STATUS=$(ORIGINAL_DIR)/status
ORIGINAL_DATA_A=$(ORIGINAL_DIR)/Supp-A-36630-HPRD-positive-interaction.txt
ORIGINAL_DATA_B=$(ORIGINAL_DIR)/Supp-B-36480-HPRD-negative-interaction.txt
ORIGINAL_DATA_C=$(ORIGINAL_DIR)/Supp-C-3899-HPRD-positive-interaction-below-0.25.txt
ORIGINAL_DATA_D=$(ORIGINAL_DIR)/Supp-D-4262-HPRD-negative-interaction-below-0.25.txt
ORIGINAL_DATA_E=$(ORIGINAL_DIR)/Supp-E-1882-interacting-0.5-non-interacting-0.5.txt

FLAT_DIR=data/01-flat
FLAT_STATUS=$(FLAT_DIR)/status
FLAT_GENERATOR=00-original2flat.py
FLAT_DATA_A=$(FLAT_DIR)/Supp-A-36630-HPRD-positive-interaction.txt
FLAT_DATA_B=$(FLAT_DIR)/Supp-B-36480-HPRD-negative-interaction.txt
FLAT_DATA_C=$(FLAT_DIR)/Supp-C-3899-HPRD-positive-interaction-below-0.25.txt
FLAT_DATA_D=$(FLAT_DIR)/Supp-D-4262-HPRD-negative-interaction-below-0.25.txt
FLAT_DATA_E=$(FLAT_DIR)/Supp-E-1882-interacting-0.5-non-interacting-0.5.txt

CT_DIR=data/02-ct
CT_STATUS=$(CT_DIR)/status
CT_GENERATOR=01-flat2ct.py
CT_DATA_A=$(CT_DIR)/Supp-A-36630-HPRD-positive-interaction.txt
CT_DATA_B=$(CT_DIR)/Supp-B-36480-HPRD-negative-interaction.txt
CT_DATA_C=$(CT_DIR)/Supp-C-3899-HPRD-positive-interaction-below-0.25.txt
CT_DATA_D=$(CT_DIR)/Supp-D-4262-HPRD-negative-interaction-below-0.25.txt
CT_DATA_E=$(CT_DIR)/Supp-E-1882-interacting-0.5-non-interacting-0.5.txt

CT_BIN_DIR=data/02-ct-bin
CT_BIN_STATUS=$(CT_BIN_DIR)/status
CT_BIN_GENERATOR=01-flat2ct-bin.py
CT_BIN_DATA_A=$(CT_BIN_DIR)/hppids-train-ppis.bin
CT_BIN_DATA_B=$(CT_BIN_DIR)/hppids-train-labels.bin
CT_BIN_DATA_C=$(CT_BIN_DIR)/hppids-test-ppis.bin
CT_BIN_DATA_D=$(CT_BIN_DIR)/hppids-test-labels.bin

AC_DIR=data/03-ac
AC_STATUS=$(AC_DIR)/status
AC_GENERATOR=02-flat2ac.py
AC_DATA_A=$(AC_DIR)/Supp-A-36630-HPRD-positive-interaction.txt
AC_DATA_B=$(AC_DIR)/Supp-B-36480-HPRD-negative-interaction.txt
AC_DATA_C=$(AC_DIR)/Supp-C-3899-HPRD-positive-interaction-below-0.25.txt
AC_DATA_D=$(AC_DIR)/Supp-D-4262-HPRD-negative-interaction-below-0.25.txt
AC_DATA_E=$(AC_DIR)/Supp-E-1882-interacting-0.5-non-interacting-0.5.txt

AC_BIN_DIR=data/03-ac-bin
AC_BIN_STATUS=$(AC_BIN_DIR)/status
AC_BIN_GENERATOR=02-flat2ac-bin.py
AC_BIN_DATA_A=$(AC_BIN_DIR)/hppids-train-ppis.bin
AC_BIN_DATA_B=$(AC_BIN_DIR)/hppids-train-labels.bin
AC_BIN_DATA_C=$(AC_BIN_DIR)/hppids-test-ppis.bin
AC_BIN_DATA_D=$(AC_BIN_DIR)/hppids-test-labels.bin

LD_DIR=data/04-ld
LD_STATUS=$(LD_DIR)/status
LD_GENERATOR=03-flat2ld.py
LD_DATA_A=$(LD_DIR)/Supp-A-36630-HPRD-positive-interaction.txt
LD_DATA_B=$(LD_DIR)/Supp-B-36480-HPRD-negative-interaction.txt
LD_DATA_C=$(LD_DIR)/Supp-C-3899-HPRD-positive-interaction-below-0.25.txt
LD_DATA_D=$(LD_DIR)/Supp-D-4262-HPRD-negative-interaction-below-0.25.txt
LD_DATA_E=$(LD_DIR)/Supp-E-1882-interacting-0.5-non-interacting-0.5.txt

LD_BIN_DIR=data/04-ld-bin
LD_BIN_STATUS=$(LD_BIN_DIR)/status
LD_BIN_GENERATOR=03-flat2ld-bin.py
LD_BIN_DATA_A=$(LD_BIN_DIR)/hppids-train-ppis.bin
LD_BIN_DATA_B=$(LD_BIN_DIR)/hppids-train-labels.bin
LD_BIN_DATA_C=$(LD_BIN_DIR)/hppids-test-ppis.bin
LD_BIN_DATA_D=$(LD_BIN_DIR)/hppids-test-labels.bin

MOS_DIR=data/05-mos
MOS_STATUS=$(MOS_DIR)/status
MOS_GENERATOR=04-flat2mos.py
MOS_DATA_A=$(MOS_DIR)/Supp-A-36630-HPRD-positive-interaction.txt
MOS_DATA_B=$(MOS_DIR)/Supp-B-36480-HPRD-negative-interaction.txt
MOS_DATA_C=$(MOS_DIR)/Supp-C-3899-HPRD-positive-interaction-below-0.25.txt
MOS_DATA_D=$(MOS_DIR)/Supp-D-4262-HPRD-negative-interaction-below-0.25.txt
MOS_DATA_E=$(MOS_DIR)/Supp-E-1882-interacting-0.5-non-interacting-0.5.txt

MOS_BIN_DIR=data/05-mos-bin
MOS_BIN_STATUS=$(MOS_BIN_DIR)/status
MOS_BIN_GENERATOR=04-flat2mos-bin.py
MOS_BIN_DATA_A=$(MOS_BIN_DIR)/hppids-train-ppis.bin
MOS_BIN_DATA_B=$(MOS_BIN_DIR)/hppids-train-labels.bin
MOS_BIN_DATA_C=$(MOS_BIN_DIR)/hppids-test-ppis.bin
MOS_BIN_DATA_D=$(MOS_BIN_DIR)/hppids-test-labels.bin

CTAC_BIN_DIR=data/09-hppids
CTAC_BIN_STATUS=$(CTAC_BIN_DIR)/status
CTAC_BIN_GENERATOR=09-to-final.py
CTAC_BIN_DATA_A=$(CTAC_BIN_DIR)/hppids-train-ppis.bin
CTAC_BIN_DATA_B=$(CTAC_BIN_DIR)/hppids-train-labels.bin
CTAC_BIN_DATA_C=$(CTAC_BIN_DIR)/hppids-test-ppis.bin
CTAC_BIN_DATA_D=$(CTAC_BIN_DIR)/hppids-test-labels.bin

.PHONY: default
default: main

$(ORIGINAL_STATUS):$(ORIGINAL_DATA_A) $(ORIGINAL_DATA_B) $(ORIGINAL_DATA_C) $(ORIGINAL_DATA_D) $(ORIGINAL_DATA_E)
	@touch -m $(ORIGINAL_STATUS)
	@echo "$(ORIGINAL_DIR) is ok"

$(FLAT_STATUS):$(FLAT_GENERATOR) $(ORIGINAL_STATUS)
	python $(FLAT_GENERATOR)
	@touch -m $(FLAT_STATUS)
	@echo "$(FLAT_DIR) is ok"

$(CT_STATUS):$(CT_GENERATOR) $(FLAT_STATUS)
	python $(CT_GENERATOR)
	@touch -m $(CT_STATUS)
	@echo "$(CT_DIR) is ok"

$(CT_BIN_STATUS):$(CT_BIN_GENERATOR) $(CT_STATUS)
	python $(CT_BIN_GENERATOR)
	@touch -m $(CT_BIN_STATUS)
	@echo "$(CT_BIN_DIR) is ok"

$(AC_STATUS):$(AC_GENERATOR) $(FLAT_STATUS)
	python $(AC_GENERATOR)
	@touch -m $(AC_STATUS)
	@echo "$(AC_DIR) is ok"

$(AC_BIN_STATUS):$(AC_BIN_GENERATOR) $(AC_STATUS)
	python $(AC_BIN_GENERATOR)
	@touch -m $(AC_BIN_STATUS)
	@echo "$(AC_BIN_DIR) is ok"

$(LD_STATUS):$(LD_GENERATOR) $(FLAT_STATUS)
	python $(LD_GENERATOR)
	@touch -m $(LD_STATUS)
	@echo "$(LD_DIR) is ok"

$(LD_BIN_STATUS):$(LD_BIN_GENERATOR) $(LD_STATUS)
	python $(LD_BIN_GENERATOR)
	@touch -m $(LD_BIN_STATUS)
	@echo "$(LD_BIN_DIR) is ok"

$(MOS_STATUS):$(MOS_GENERATOR) $(FLAT_STATUS)
	python $(MOS_GENERATOR)
	@touch -m $(MOS_STATUS)
	@echo "$(MOS_DIR) is ok"

$(MOS_BIN_STATUS):$(MOS_BIN_GENERATOR) $(MOS_STATUS)
	python $(MOS_BIN_GENERATOR)
	@touch -m $(MOS_BIN_STATUS)
	@echo "$(MOS_BIN_DIR) is ok"

$(CTAC_BIN_STATUS):$(CTAC_BIN_GENERATOR) $(CT_STATUS) $(AC_STATUS)
	python $(CTAC_BIN_GENERATOR)
	@touch -m $(CTAC_BIN_STATUS)
	@echo "$(CTAC_BIN_DIR) is ok"

.PHONY:data
data: $(CT_BIN_STATUS) $(AC_BIN_STATUS) $(LD_BIN_STATUS) $(MOS_BIN_STATUS) $(CTAC_BIN_STATUS)

.PHONY:main
main: data
