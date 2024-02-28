# Targets

build:
	python -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r scripts/app/util/requirements.txt 
.PHONY: build

updateStats: build updateTeams updateRounds
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

clean:
	rm -rf .venv
.PHONY: clean
