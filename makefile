# Targets

build:
	python3.11 -m venv .venv && \
	source .venv/bin/activate && \
	pip3.11 install --upgrade pip && \
	pip3.11 install -r requirements.txt 
.PHONY: build

deploy: build
	. .venv/bin/activate && \
	cd dynamodb; cdk deploy; cd .. && \
	python3.11 scripts/update_ladder.py
.PHONY: deploy

updateLadder: build
	. .venv/bin/activate && \
	python3.11 scripts/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	. .venv/bin/activate && \
	python3.11 scripts/update_teams.py
.PHONY: updateTeams


destroy:
	. .venv/bin/activate && \
	cd dynamodb; cdk destroy; cd .. && \
	rm -rf .venv
.PHONY: destroy
