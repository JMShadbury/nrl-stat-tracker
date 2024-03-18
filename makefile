# Variables
VENV_ACTIVATE = . venv/bin/activate &&
PYTHON = python
PIP = pip
MKDIR_P = mkdir -p
CP_R = cp -r
RM_RF = rm -rf
TAR_CZVF = tar -czvf
TAR_XZVF = tar -xzvf
OPENSSL_ENC = openssl enc
AWS_S3_CP = aws s3 cp
FIND = find
AWK = awk
RM_EMPTY_DIR = $(FIND) backup/ -type d -empty -delete
JSON_FILES := $(wildcard app/teams/*.json)

ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = venv\Scripts\activate &&
	PYTHON = py
	MKDIR_P = mkdir $(subst /,\,$(dir $@)) > nul 2>&1 || true
	CP_R = xcopy /s /e
	RM_RF = rmdir /s /q
	TAR_CZVF = tar -czvf
	TAR_XZVF = tar -xzvf
	OPENSSL_ENC = openssl enc
	AWS_S3_CP = aws s3 cp
	FIND = dir /b /ad /s
	AWK = awk
	RM_EMPTY_DIR = $(FIND) backup\ -type d -empty | $(AWK) '{ print "rmdir /s /q \"" $$0 "\"" }' | cmd
endif

# Targets
.PHONY: all build updateStats updateTeams updateRounds getData run clean cleanAll fresh backup getBackup pre-backup encryptBackup decryptBackup uploadBackup downloadBackup restoreBackup cleanBackup prep-upload

all: fresh

build:
	$(PYTHON) -m venv venv && \
	$(VENV_ACTIVATE) \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt

updateStats: build updateTeams
	$(VENV_ACTIVATE) $(PYTHON) scrape/update_ladder.py

updateTeams: build
	$(VENV_ACTIVATE) $(PYTHON) scrape/update_teams.py

updateRounds: build
	$(VENV_ACTIVATE) $(PYTHON) scrape/update_rounds.py

getData: build updateStats
	$(VENV_ACTIVATE) $(PYTHON) scrape/get_data.py

run: build $(if $(JSON_FILES),,getData)
	$(VENV_ACTIVATE) cd app && $(PYTHON) view_stats.py

clean:
	$(RM_RF) venv logs app/logs __pycache__ common/__pycache__ app/__pycache__ app/teams/__pycache__ app/rounds/__pycache__ app/ladder/__pycache__ app/util/__pycache__ scrape/__pycache__ scrape/all_data/__pycache__ scrape/util/__pycache__ scrape/stats/__pycache__

cleanAll: clean
	$(RM_RF) scrape/all_data/* app/teams/*.json app/rounds app/ladder backup/

tryCleanAll:
	@$(MAKE) cleanAll 2>/dev/null || true

fresh: tryCleanAll build getData run

backup: pre-backup encryptBackup prep-upload uploadBackup cleanBackup

getBackup: downloadBackup decryptBackup restoreBackup cleanBackup

pre-backup:
	$(MKDIR_P) "backup/$(round)"
	$(CP_R) app/teams app/ladder scrape/all_data "backup/$(round)"

encryptBackup:
	$(TAR_CZVF) "backup/$(round).tar.gz" -C "backup/" "$(round)" && \
	$(OPENSSL_ENC) -aes-256-cbc -pbkdf2 -iter 10000 -salt -in "backup/$(round).tar.gz" -out "backup/$(round).tar.gz.encrypted" -pass file:/Users/joelhutson/.pers/personal

decryptBackup:
	$(OPENSSL_ENC) -d -aes-256-cbc -pbkdf2 -iter 10000 -in "backup/$(round).tar.gz.encrypted" -out "backup/$(round).tar.gz" -pass file:/Users/joelhutson/.pers/personal && \
	$(TAR_XZVF) "backup/$(round).tar.gz" -C "backup/$(round)/" && \
	$(RM_RF) "backup/$(round).tar.gz" "backup/$(round).tar.gz.encrypted"

uploadBackup:
	$(AWS_S3_CP) "backup/$(round).tar.gz.encrypted" s3://2024-nrl-data/$(round)/$(round).tar.gz.encrypted --profile $(AWS_PROFILE)

downloadBackup:
	$(AWS_S3_CP) s3://2024-nrl-data/$(round) backup/$(round) --recursive --profile $(AWS_PROFILE)

restoreBackup:
	$(CP_R) "backup/$(round)/teams" app/ && \
    $(CP_R) "backup/$(round)/ladder" app/ && \
    $(CP_R) "backup/$(round)/all_data" scrape/

cleanBackup:
	$(RM_RF) backup
	$(RM_EMPTY_DIR)

prep-upload:
	$(FIND) backup/ -type f ! -name "*.encrypted" -delete
	$(RM_EMPTY_DIR)
