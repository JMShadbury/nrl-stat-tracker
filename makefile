# Targets

build:
	python -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt 
.PHONY: build

updateStats: build updateTeams
	. venv/bin/activate && \
	python scrape/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	. venv/bin/activate && \
	python scrape/update_teams.py
.PHONY: updateTeams

updateRounds: build
	. venv/bin/activate && \
	python scrape/update_rounds.py

getData: build updateStats 
	. venv/bin/activate && \
	python scrape/get_data.py
.PHONY: getData

viewStats: build
	. venv/bin/activate && \
	cd app && \
	python view_stats.py

clean:
	rm -rf venv
	rm -rf logs
	rm -rf app/logs
	rm -rf __pycache__
	rm -rf common/__pycache__
	rm -rf app/__pycache__
	rm -rf app/teams/__pycache__
	rm -rf app/rounds/__pycache__
	rm -rf app/ladder/__pycache__
	rm -rf app/util/__pycache__
	rm -rf scrape/__pycache__
	rm -rf scrape/all_data/__pycache__
	rm -rf scrape/util/__pycache__
	rm -rf scrape/stats/__pycache__
.PHONY: clean

cleanAll: clean
	rm -rf scrape/all_data/*
	rm -rf app/teams/*.json
	rm -rf app/rounds
	rm -rf app/ladder
	rm -rf backup/
.PHONY: cleanAll

tryCleanAll: 
	@$(MAKE) cleanAll 2>/dev/null || true
.PHONY: tryCleanAll

fresh: tryCleanAll build getData
	make viewStats
.PHONY: fresh

backup:
	@$(MAKE) pre-backup round=$(round)
	@$(MAKE) encryptBackup round=$(round)
	@$(MAKE) prep-upload round=$(round)
	@$(MAKE) uploadBackup round=$(round)
	@$(MAKE) cleanBackup
.PHONY: backupTest

getBackup:
	@$(MAKE) downloadBackup round=$(round)
	@$(MAKE) decryptBackup round=$(round)
	@$(MAKE) restoreBackup round=$(round)
.PHONY: getBackup

pre-backup:
	mkdir -p "backup/$(round)" && \
	cp -r app/teams "backup/$(round)" && \
	cp -r app/ladder "backup/$(round)" && \
	cp -r scrape/all_data "backup/$(round)"
.PHONY: backup

encryptBackup:
	@if [ -z "$(round)" ]; then echo "Error: No round specified for backup"; exit 1; fi
	tar -czvf "backup/$(round).tar.gz" -C "backup/" "$(round)" && \
	openssl enc -aes-256-cbc -pbkdf2 -iter 10000 -salt -in "backup/$(round).tar.gz" -out "backup/$(round).tar.gz.encrypted" -pass file:/Users/joelhutson/.pers/personal
.PHONY: encryptBackup


decryptBackup:
	openssl enc -d -aes-256-cbc -pbkdf2 -iter 10000 -in "backup/$(round)/$(round).tar.gz.encrypted" -out "backup/$(round)/$(round).tar.gz" -pass file:/Users/joelhutson/.pers/personal && \
	tar -xzvf "backup/$(round)/$(round).tar.gz" -C "backup/$(round)/" && \
	rm "backup/$(round)/$(round).tar.gz" "backup/$(round)/$(round).tar.gz.encrypted"
.PHONY: decryptBackup

uploadBackup:
	aws s3 cp "backup/$(round).tar.gz.encrypted" s3://2024-nrl-data/$(round)/$(round).tar.gz.encrypted --profile joeladmin
.PHONY: uploadBackup

downloadBackup:
	aws s3 cp s3://2024-nrl-data/$(round) backup/$(round) --recursive --profile joeladmin
.PHONY: downloadBackup

restoreBackup:
	cp -r "backup/$(round)/$(round)/teams" app/ && \
    cp -r "backup/$(round)/$(round)/ladder" app/ && \
    cp -r "backup/$(round)/$(round)/all_data" scrape/
.PHONY: restoreBackup

cleanBackup:
	rm -rf backup/*
.PHONY: cleanBackup

prep-upload:
	find backup/ -type f ! -name "*.encrypted" -delete
	find backup/ -type d -empty -delete
.PHONY: prep-upload