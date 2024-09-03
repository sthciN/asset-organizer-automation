# Overview
This project provides a robust solution for asset reorganization and processing using Python, Google APIs, and Docker. It integrates with Google Drive and Sheets to manage assets, performs validations, and processes images based on predefined criteria. The system is designed to handle large volumes of data efficiently and is built with scalability in mind.

# Features
## Feature 1: Asset Reorganization
1. Read Settings

The script reads settings from a Google Spreadsheet (UI tab).
It reorganizes files on Google Drive based on the levels specified.
To avoid nested folder conflicts when levels change, update the NEW_FOLDER_ID in the environment variables.

2. Reorganize Assets

    1. Backup and Reorganization
        
        Each time the script runs, it keeps a backup of the homework_items Drive folder and reorganizes them in the folder with the id set as NEW_FOLDER_ID in the `.env`.

    2. The script duplicates files to the new folder called `Backup Folder`, It creates this folder if it doesn't exist.
    3. Files with the same name are not duplicated; they are moved if needed.
    4. Assets fetched are .png files and resized to <100kb.

## Feature 2: Asset Processing
### Validate Assets

- Naming Validation: Assets are validated against a regex pattern.
- Buyout Expiration Check: Expired assets are detected using their buyout code (referenced from the buyouts sheet). Their budget is set to zero using the mocked API, with retry logic (3 attempts with delay).
- Quality Check: Images are analyzed using the mocked OpenAI API. Only images with quality > 5 and privacy_compliant: True proceed.


### Provide Feedback

- Logging: Logs the names of the assets into a specified sheet named as Logs-{starting-process-datetime}, different worksheets made for validation failure in the LOG_FOLDER_ID.
- Error Handling: New logs are created for each run, allowing for tracking of file processing status.

## Deployment

1. Setup Environment Variables

Create a `.env` file with the following variables:
```
PNG_FOLDER_ID: The ID of the folder where the original assets are located.
DATA_FOLDER_ID: The ID of the folder where the data sheet (Vinted Homework.2) is located.
DATA_SHEET_NAME: The name of the Data sheet (Vinted Homework.2)
NEW_FOLDER_ID: The ID of the new folder where files will be reorganized.
LOG_FOLDER_ID: The ID of the folder where logs will be written.
GOOGLEADS_API_KEY: The API key used for Googleads API.
OPENAI_API_KEY: The API key used for OpenAI API.
POSTGRES_USER: The PostgreSQL username.
POSTGRES_PASSWORD: The PostgreSQL password
POSTGRES_DB: The name of the PostgreSQL database.
```
2. Copy your [`service_account.json`](#google-api-setup) into the credentials folder.
3. Run `docker-compose up --build` to build and start the Docker containers.
4. Access Frontend at `http://localhost:3000/`.

### Frontend
After clicking on the `Start the Process`, a task starts in background in the backend service. It process all the assets in the PNG_FOLDER_ID. The fronend has a polling mechanism that requests the status of the task. If it becomes completed the `Start the Process` buttons will be enabled again for a fresh processing. Other wise user will see the processing is still in progress. The `Fetch File List` button is only for seeing the files in the PNG_FOLDER_ID.

### Technical Details
- Backend: FastAPI that handles the processing task in background.
- Frontend: React
- Database: PostgreSQL (chosen for multithreading capabilities)
- Programming Language: Python 3.12
- Libraries:
    - `Pillow` for resizing the image
    - `google-api-python-client` for Google Drive
    - `gspread` for Google Sheets
    - `pandas` for data manipulation

### Google API Setup

1. Enable APIs

- [Google Drive API](https://console.cloud.google.com/apis/enableflow?apiid=drive.googleapis.com)
- [Google Sheets API](https://console.cloud.google.com/apis/enableflow?apiid=sheets.googleapis.com)

2. Generate Key
    Create a service account and add the client email to the data sheet (Vinted Homework.2). 

3. Add Creds
    Move the generated key to the credentials folder and rename it to `service_account.json`.


## Known Issues and Considerations
- Parallelism: Google Drive APIs do not handle parallelism well, leading to SSL and authorization errors in multithreading. To address this, consider using a database with ACID properties for parallelism support.
- Validation Process: Validations are performed sequentially. Future improvements could include parallel validation processes.

## Assumptions
- File Naming and Asset Management: Instead of asset or asset_id, I used file and file_id across the app for clear and consistent naming. 
- The asset names do not relate to ad_id in uac_ads_data. Static ad_id are used for budget updates.
- Expiration Check: Files with D0000 are considered expired if the current date is beyond 02/09/2024.
- Validation Order: Validations are assumed to occur in sequence and are not parallelized.

## Future Improvements
- Logging Enhancements: Consider a separate threaded logging for improved performance.
- Parallel Processing: Implement parallelism by using databases for logging and create a task queue for each file
