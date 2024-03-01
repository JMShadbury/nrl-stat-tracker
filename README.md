
# NRL Stat Tracker

## Description
NRL Stat Tracker is an application designed to collect, analyze, and display statistics from NRL (National Rugby League) matches. It utilizes a combination of technologies including [specific languages, frameworks, libraries, etc.], making it a robust and efficient tool for NRL enthusiasts and analysts.

## Features
- Real-time statistics tracking from NRL matches.
- Data visualization tools for in-depth analysis.
- Easy integration with DynamoDB for data storage and retrieval.
- Customizable scripts for various analytical needs.

## Installation
To install NRL Stat Tracker, follow these steps:

1. Clone the repository:
   ```
   git clone [repository URL]
   ```
2. Navigate to the project directory:
   ```
   cd nrl-stat-tracker
   ```
3. [Any additional installation steps like setting up a virtual environment, installing dependencies, etc.]

## Usage
Everything is setup using makefile.

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
.PHONY: clean

The list of commands are:
- `make build` - This will create a virtual environment and install all the dependencies.
- `make updateStats` - This will update the ladder, teams and rounds.
- `make updateTeams` - This will update the teams.
- `make updateRounds` - This will update the rounds.
- `make getData` - This will get the data from the NRL website.
- `make viewStats` - This will display the stats.
- `make clean` - This will remove the virtual environment and logs.

#! Note: Running make getData will run all required commands to get the data from the NRL website. After this is done, you can run make viewStats to view the stats.

## Contributing
Contributions to NRL Stat Tracker are welcome. Please adhere to the following guidelines:

- Fork the repository and create your branch from `master`.
- Write clear and concise commit messages.
- Ensure code style and quality standards are maintained.
- Create a pull request with a detailed description of changes.

## License
This project is licensed under the [License Name]. Please see the [LICENSE](LICENSE) file for more details.
