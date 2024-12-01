# Backup PostgreSQL to Google Drive

This project provides a Dockerized solution to back up a PostgreSQL database and upload the backup file to Google Drive.

## Prerequisites

- Docker
- Google Cloud Service Account with Google Drive API enabled

## Setup

1. Pull the Docker image:
    ```bash
    docker pull appzic/backup-psql-to-gdrive
    ```

2. Set the following environment variables:
    - `DB_NAME`: Your PostgreSQL database name
    - `DB_USER`: Your PostgreSQL database user
    - `DB_PASSWORD`: Your PostgreSQL database password
    - `DB_HOST`: Your PostgreSQL database host
    - `GDRIVE_FOLDER_ID`: Your Google Drive folder ID where the backup will be uploaded
    - `GDRIVE_AUTH_KEY`: Path to your Google Drive service account credentials JSON file

## Usage

1. Run the Docker container with the environment variables:
    ```bash
    docker run -e DB_NAME=your_db_name \
               -e DB_USER=your_db_user \
               -e DB_PASSWORD=your_db_password \
               -e DB_HOST=your_db_host \
               -e GDRIVE_FOLDER_ID=your_gdrive_folder_id \
               -e GDRIVE_AUTH_KEY=/path/to/your/credentials.json \
               appzic/backup-psql-to-gdrive
    ```

2. The backup script will run and upload the PostgreSQL database backup to the specified Google Drive folder.

## License

This project is licensed under the MIT License.