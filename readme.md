# Project Overview

This project automates the process of downloading data from 13,000 files, validating them, and merging the data into a single file.

## How It Works

1. **Progress Monitoring**:
   - Run `validate.py` to generate an array object that tracks the progress of each file.

2. **Downloading Files**:
   - Run `main.py` to start a Selenium browser instance and download the Excel files.

3. **Data Recap**:
   - Once all files are downloaded, open and run the Jupyter Notebook `data_recap.ipynb` to extract and combine data from each file into one file using Pandas.

## Setup Instructions

1. **Create a Virtual Environment**:
   - Using `pip` and `venv`:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     pip install -r requirements.txt
     ```
   - Using `pipenv`:
     ```bash
     pipenv install
     ```

2. Install the required dependencies as listed in `requirements.txt`.

## Tools Used

- **Python**
- **Selenium** for browser automation
- **Pandas** for data manipulation

## Notes

- Ensure all dependencies are installed before running the scripts.
- This project simplifies handling large datasets and streamlines the process into a few clear steps.

