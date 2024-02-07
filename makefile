# Targets

build:
	pip install --upgrade pip && \
	pip install -r scripts/app/util/requirements.txt 
.PHONY: build

deploy: build
	cd dynamodb; cdk deploy
.PHONY: deploy

deployApp: build
	cd nrl_app; cdk deploy
.PHONY: deployApp

deployAll: build deploy updateLadder updateTeams getData viewStats
.PHONY: deployAll

updateLadder: build
	python scripts/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	python scripts/update_teams.py
.PHONY: updateTeams

getData: build
	python scripts/get_data.py
.PHONY: getData

viewStats: build
	python scripts/view_stats.py

destroy:
	cd dynamodb; cdk destroy; cd .. && \
	rm -rf .venv
.PHONY: destroy

clean:
	rm -rf .venv
.PHONY: clean
