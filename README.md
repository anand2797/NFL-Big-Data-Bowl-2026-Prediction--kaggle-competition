
# NFL-Big-Data-Bowl-2026-Prediction--kaggle-competition
Kaggle competition project for the 2026 NFL Big Data Bowl. Predicts future x/y positions of NFL players after a pass using player tracking data. Includes data preprocessing, feature engineering, sequence modeling, predictions, and submission generation.


## 1. Project Structure Automation

This repository includes a `templates.py` script that automatically generates the recommended file and directory structure for the NFL Game Competition project.

### Usage

Run `templates.py` to create all necessary folders and files for the project. This helps maintain consistency and saves setup time for new contributors.

**How it works:**
- The script creates directories and empty files as defined in its `list_of_files` variable.
- It uses Python's `os` and `pathlib` modules for cross-platform compatibility.
- Logging messages indicate which files and folders are created or already exist.

**To run:**
```bash
python templates.py
```


## 2. Connecting to a Git Repository

Below are all possible ways to connect your local project to a git repository:

### a) Before Starting the Project: Clone the Repository
If you want to start with an existing remote repository, use:
```bash
git clone <repo-url>
cd <repo-folder>
```
This will copy all files from the remote repository to your local machine.

### b) After Running templates.py: Pull Latest Files
If you have already generated the project structure locally and want to sync with a remote repository:
```bash
git init
git remote add origin <repo-url>
git fetch origin
git pull origin master  # or main, depending on branch name
```
This will initialize git, connect to the remote, and pull files.

### c) No Files in Repo: Add Files and Push to Remote
If your remote repository is empty and you want to add your local files:
```bash
git init
git remote add origin <repo-url>
git add .
git commit -m "Initial project structure"
git branch -M master  # or main
# If the remote is empty, you may need to force push:
git push -u origin master  # or main
```
This will add all files, commit, and push them to the remote repository.

> **Note:** Replace `<repo-url>` with your actual repository URL and use the correct branch name (`master` or `main`).
