# Targets

build:
	pip install --upgrade pip && \
	pip install -r scripts/app/util/requirements.txt 
.PHONY: build

deployBackend: build
	cd backend; cdk deploy --all --require-approval never
.PHONY: deployApp

updateStats: build updateTeams
	python scripts/scrape/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	python scripts/scrape/update_teams.py
.PHONY: updateTeams

updateRounds: build
	python scripts/scrape/update_rounds.py

getData: build
	python scripts/scrape/get_data.py
.PHONY: getData

viewStats: build
	python scripts/app/view_stats.py

destroy:
	cd dynamodb; cdk destroy; cd .. && \
	rm -rf .venv
.PHONY: destroy

clean:
	rm -rf .venv
.PHONY: clean
