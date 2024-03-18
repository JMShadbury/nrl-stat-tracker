
# NRL Stat Tracker

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)
6. [Contribution Guidelines](#contribution-guidelines)
7. [License](#license)

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

2. **Windows**:
    - Install Chocolatey (if not already installed):
       - Open PowerShell as Administrator and run the following command:
          ```shell
          Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
          ```
    - Install Make using Chocolatey:
       - Open PowerShell as Administrator and run the following command:
          ```shell
          choco install make

<a name="usage"></a>
## Usage
<details>
<summary>Click to expand!</summary>


To use the NRL Stat Tracker, follow these guidelines based on the provided `makefile`:

1. **Build the Project**: 
   - Run `make build` to set up a Python virtual environment, upgrade pip, and install required dependencies from `requirements.txt`.

2. **Update Statistics**: 
   - Use `make updateStats` to update team statistics. This command first builds the project and then updates the teams and ladder information.

3. **Get Data**: 
   - Run `make getData` to retrieve all necessary data for the application. This command builds the project, updates stats, and fetches additional data.

4. **View Statistics**: 
   - Execute `make viewStats` to start the application for viewing statistics.

5. **Clean the Project**:
   - `make clean` removes the virtual environment and temporary files.
   - `make cleanAll` performs a more comprehensive clean-up, including all data and logs.

6. **Backup and Restore**:
   - Use targets like `make backup` and `make restoreBackup` for handling backups and restoration of data.

7. **Testing**:
   - The `make test` command runs a series of operations to build the project, update stats, get data, and view stats as a part of testing.
</details>

<a name="contribution-guidelines"></a>
## Contribution Guidelines
We welcome contributions! Here's how you can contribute to this project effectively.

<a name="license"></a>
## License
Details on the project's licensing and usage terms.

---
© NRL Stat Tracker Team
