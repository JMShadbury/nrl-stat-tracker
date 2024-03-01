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

getData: build updateStats cleanAll
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
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf app/teams/__pycache__
	rm -rf app/rounds/__pycache__
	rm -rf app/ladder/__pycache__
	rm -rd app/util/__pycache__
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
.PHONY: cleanAll
