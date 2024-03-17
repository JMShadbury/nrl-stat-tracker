
# NRL Stat Tracker

## Introduction
NRL Stat Tracker is an advanced application designed for collecting, analyzing, and displaying statistics from NRL (National Rugby League) matches. It caters to enthusiasts, analysts, and anyone keen on deep rugby match insights.

## Features
- **Real-time Statistics Tracking**: Captures and displays live stats from NRL matches.
- **Data Visualization**: Features advanced tools for insightful analysis of match data.
- **Custom Scoring System**: Utilizes a unique algorithm for evaluating performance.
- **Web Interface**: Offers a user-friendly interface for easy access to statistics.
- **Data Scraping and Management**: Efficiently collects and processes data from various sources.

## Technologies Used
- **Python**: For backend processing, data analysis, and scraping.
- **HTML/CSS & Bootstrap**: Powers the front-end for a responsive web experience.
- **JavaScript**: Enhances the interactivity of the web interface.

## Installation and Setup
Instructions on setting up the application for smooth and efficient operation.

## Usage
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

Each of these commands should be run from the root directory of the project. The `makefile` is designed to streamline the setup, operation, and maintenance of the NRL Stat Tracker, making it efficient and user-friendly.

## Contribution Guidelines
We welcome contributions! Here's how you can contribute to this project effectively.

## License
Details on the project's licensing and usage terms.

---
© NRL Stat Tracker Team
