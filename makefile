# Targets

build:
	python3.11 -m venv .venv && \
	source .venv/bin/activate && \
	pip3.11 install --upgrade pip && \
	pip3.11 install -r scripts/util/requirements.txt 
.PHONY: build

deploy: build
	. .venv/bin/activate && \
	cd dynamodb; cdk deploy
.PHONY: deploy

deployAll: build deploy updateLadder updateTeams getData viewStats
.PHONY: deployAll

updateLadder: build
	. .venv/bin/activate && \
	python3.11 scripts/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	. .venv/bin/activate && \
	python3.11 scripts/update_teams.py
.PHONY: updateTeams

getData: build
	. .venv/bin/activate && \
	python3.11 scripts/get_data.py
.PHONY: getData

viewStats: build
	. .venv/bin/activate && \
	python3.11 scripts/view_stats.py

destroy:
	. .venv/bin/activate && \
	cd dynamodb; cdk destroy; cd .. && \
	rm -rf .venv
.PHONY: destroy

clean:
	rm -rf .venv
.PHONY: clean
