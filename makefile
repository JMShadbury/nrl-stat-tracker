# Variables
VENV_ACTIVATE = . venv/bin/activate &&
PYTHON = python
PIP = pip
MKDIR_P = mkdir -p
CP_R = cp -r
RM_RF = rm -rf
AWS_S3_CP = aws s3 cp
FIND = find
AWK = awk
RM_EMPTY_DIR = $(FIND) backup/ -type d -empty -delete
JSON_FILES := $(wildcard app/teams/*.json)

# Targets
.PHONY: all build updateStats updateTeams updateRounds getData run clean cleanAll fresh backup getBackup pre-backup uploadBackup downloadBackup restoreBackup cleanBackup prep-upload

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

getData: build updateStats
	$(VENV_ACTIVATE) $(PYTHON) scrape/get_data.py

run: build $(if $(JSON_FILES),,getData)
	$(VENV_ACTIVATE) cd app && $(PYTHON) view_stats.py

clean:
	$(RM_RF) venv logs app/logs __pycache__ common/__pycache__ app/__pycache__ app/teams/__pycache__ app/rounds/__pycache__ app/ladder/__pycache__ app/util/__pycache__ scrape/__pycache__ scrape/all_data/__pycache__ scrape/util/__pycache__ scrape/stats/__pycache__ geckodriver.log

cleanAll: clean
	$(RM_RF) scrape/all_data/* app/teams/ app/rounds app/ladder backup/

tryCleanAll:
	@$(MAKE) cleanAll 2>/dev/null || true

fresh: tryCleanAll build getData run

getBackup: downloadBackup restoreBackup cleanBackup

downloadBackup:
	$(AWS_S3_CP) --recursive s3://2024-nrl-data/$(ROUND_NUMBER)/ "backup/$(ROUND_NUMBER)" 

restoreBackup:
	$(CP_R) "backup/$(ROUND_NUMBER)/teams" app/ && \
	$(CP_R) "backup/$(ROUND_NUMBER)/ladder" app/ && \
	$(CP_R) "backup/$(ROUND_NUMBER)/all_data" scrape/

cleanBackup:
	@if [ -d "backup/" ]; then \
		$(FIND) backup/ -type d -empty -delete; \
	fi
	$(RM_EMPTY_DIR)