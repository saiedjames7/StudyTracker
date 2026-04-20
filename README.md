# Study Tracker Application

## Overview

The Study Tracker is a Python-based application designed to help students manage and organise their study sessions effectively. It allows users to create accounts and track their study activity in a structured way.

## Target Users

This application is intended for students, including:

* GCSE students
* A-Level students
* University students

## Features

### User Management

* Create an account (write user data)
* View account details (read user data)

### Study Session Management

* Create study sessions
* View study sessions
* Update study sessions
* Delete study sessions

### Core Functionality

* User authentication system to manage login and access
* Main interface (GUI) for interacting with the application

## Technical Requirements

* Python (version 3.x recommended)
* Virtual environment (venv)
* CustomTkinter installed

## How to Run the Program

1. Extract the Zip Folder
   
2. Open a terminal and navigate to the project folder

3. Ensure you are in the same directory as the `venv` folder

4. I recommend running in a virtual environment. You can activate the virtual environment by doing:

   On macOS/Linux:

   ```
   source venv/bin/activate
   ```

5. Run the program:

   ```
   python main.py
   ```

## Data Storage

The program automatically generates the following files when run:

* `users.csv` – stores user account information
* `sessions.csv` – stores study session data

## Development Tools

### Version Control

Git was used for version control throughout development. Changes were committed regularly and pushed to GitHub to track progress and maintain version history.

### AI Tools

Claude was used during development to:

* Suggest code structure
* Help identify and fix errors
* Help write some lines of code

ChatGPT was used to help write this ReadMe File

All AI-generated suggestions were reviewed and adapted where necessary.

## Enhancements

The application includes the following enhancements:

* Persistent data storage using CSV files
* Structured user interface for ease of use

## Known Limitations

* Requires manual activation of the virtual environment before running
* Data is stored locally (no cloud storage or backup)

## Notes for Marker

Please ensure the virtual environment is activated before running the program. The application will automatically generate required data files if they do not already exist.
