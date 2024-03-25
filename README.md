
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
    - Install Python 3 using Homebrew:
         ```shell
         brew install python
         ```

<a name="usage"></a>

## Usage
<details>
<summary>Click to expand!</summary>

To use the NRL Stat Tracker, follow these guidelines based on the provided `makefile`:

1. **Build the Project**: 
   - Run `make build` to set up a Python virtual environment, upgrade pip, and install required dependencies from `requirements.txt`.

2. **Update Statistics**: 
   - Use `make updateStats` to update team statistics. This command builds the project and then updates the teams and ladder information.

3. **Update Teams**:
   - Run `make updateTeams` to specifically update team data. This command also involves building the project.

4. **Update Rounds**:
   - Use `make updateRounds` to update round-specific information. This command first builds the project.

5. **Get Data**: 
   - Run `make getData` to retrieve all necessary data for the application. This command builds the project, updates stats, and fetches additional data.

6. **Run Application**:
   - Execute `make run` to start the application. It builds the project, gets data if not present, and launches the app for viewing statistics.

7. **Clean the Project**:
   - `make clean` removes the virtual environment and temporary files.
   - `make cleanAll` performs a more comprehensive clean-up, including all data and logs.

8. **Attempt to Clean All**:
   - Run `make tryCleanAll` to attempt a full cleanup; suppresses error messages if any steps fail.

9. **Start Fresh**:
   - Use `make fresh` to clean the project completely and start fresh by building the project and fetching new data.

10. **Backup and Restore**:
   - `make backup` handles backup creation, encryption, and uploading to storage.
   - `make getBackup` downloads, decrypts, and restores data from the backup.
   - `make uploadBackup` and `make downloadBackup` specifically handle uploading and downloading backups.
   - `make encryptBackup` and `make decryptBackup` are used for encrypting and decrypting backups.
   - `make restoreBackup` and `make cleanBackup` are used to restore data from backups and clean up backup files, respectively.

11. **Prepare for Backup Upload**:
   - `make prep-upload` prepares for uploading the backup by cleaning up unnecessary files.

</details>


<a name="contribution-guidelines"></a>
## Contribution Guidelines
We welcome contributions! Here's how you can contribute to this project effectively.

<a name="license"></a>
## License
Details on the project's licensing and usage terms.

---
© NRL Stat Tracker Team
