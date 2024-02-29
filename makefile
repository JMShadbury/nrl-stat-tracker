# Targets

build:
	python -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r app/util/requirements.txt 
.PHONY: build

updateStats: build updateTeams updateRounds
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

getData: build
	. venv/bin/activate && \
	python scrape/get_data.py
.PHONY: getData

viewStats: build
	. venv/bin/activate && \
	cd app && \
	python view_stats.py

clean:
	rm -rf .venv
.PHONY: clean
