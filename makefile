# Targets

build:
	python -m venv .venv && \
	source .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r scripts/app/requirements.txt 
.PHONY: build

deploy: build
	. .venv/bin/activate && \
	cd dynamodb; cdk deploy
.PHONY: deploy

deployApp: build
	. .venv/bin/activate && \
	cd nrl_app; cdk deploy
.PHONY: deployApp

deployAll: build deploy updateLadder updateTeams getData viewStats
.PHONY: deployAll

updateLadder: build
	. .venv/bin/activate && \
	python scripts/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	. .venv/bin/activate && \
	python scripts/update_teams.py
.PHONY: updateTeams

getData: build
	. .venv/bin/activate && \
	python scripts/get_data.py
.PHONY: getData

viewStats: build
	. .venv/bin/activate && \
	python scripts/view_stats.py

destroy:
	. .venv/bin/activate && \
	cd dynamodb; cdk destroy; cd .. && \
	rm -rf .venv
.PHONY: destroy

clean:
	rm -rf .venv
.PHONY: clean
