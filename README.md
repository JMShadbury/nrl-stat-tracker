
# NRL Stat Tracker

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)

<a name="introduction"></a>
## Introduction
NRL Stat Tracker is an advanced application designed for collecting, analyzing, and displaying statistics from NRL (National Rugby League) matches. It caters to enthusiasts, analysts, and anyone keen on deep rugby match insights.

<a name="features"></a>
## Features
- **Real-time Statistics Tracking**: Captures and displays live stats from NRL matches.
- **Data Visualization**: Features advanced tools for insightful analysis of match data.
- **Custom Scoring System**: Utilizes a unique algorithm for evaluating performance.
- **Web Interface**: Offers a user-friendly interface for easy access to statistics.
- **Data Scraping and Management**: Efficiently collects and processes data from various sources.

<a name="technologies-used"></a>
## Technologies Used
- **Python**: For backend processing, data analysis, and scraping.
- **HTML/CSS & Bootstrap**: Powers the front-end for a responsive web experience.
- **JavaScript**: Enhances the interactivity of the web interface.

<a name="installation-and-setup"></a>
## Installation and Setup
1. **Mac**:
    - Install Homebrew (if not already installed):
       ```shell
       /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
       ```
    - Install Make using Homebrew:
       ```shell
       brew install make
       ```
    - Install Python 3 using Homebrew:
         ```shell
         brew install python
         ```

<a name="usage"></a>

## Usage

To run the application, use the following command:
**Run Application**:
   - Execute `make run` to start the application. It builds the project, gets data if not present, and launches the app for viewing statistics.

<details>
<summary>More options - Click to expand!</summary>

To use the NRL Stat Tracker, follow these guidelines based on the provided `makefile`:

1. **Build the Project**: 
   - Run `make build` to set up a Python virtual environment, upgrade pip, and install required dependencies from `requirements.txt`.

2. **Update Statistics**: 
   - Use `make updateStats` to update team statistics. This command builds the project and then updates the teams and ladder information.

3. **Update Teams**:
   - Run `make updateTeams` to specifically update team data. This command also involves building the project.

4. **Get Data**: 
   - Run `make getData` to retrieve all necessary data for the application. This command builds the project, updates stats, and fetches additional data.

5. **Clean the Project**:
   - `make clean` removes the virtual environment and temporary files.
   - `make cleanAll` performs a more comprehensive clean-up, including all data and logs.

6. **Start Fresh**:
   - Use `make fresh` to clean the project completely and start fresh by building the project and fetching new data.

</details>


<a name="status"></a>

## Status

Python Linting:

![lint workflow](https://github.com/github/docs/actions/workflows/pylint.yml/badge.svg?event=push)

NRL Backups:
![backup workflow](https://github.com/github/docs/actions/workflows/rounds.yml/badge.svg?event=push)
