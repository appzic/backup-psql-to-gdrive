import os
import subprocess
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

def backup_postgresql(db_name, db_user, db_password, db_host, db_port=5432):
    os.environ['PGPASSWORD'] = db_password
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'{db_name}_{timestamp}.sql'
    dump_command = f'pg_dump -h {db_host} -U {db_user} -d {db_name} -p {db_port} --no-owner --no-privileges --inserts  > {backup_file}'
    subprocess.call(dump_command, shell=True)
    del os.environ['PGPASSWORD']
    print(f'Backup created: {backup_file}')
    return backup_file

def upload_to_gdrive(file_path, gdrive_folder_id, gdrive_auth_domain_wide_delegation = None):
    
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    if gdrive_auth_domain_wide_delegation:
        credentials = credentials.with_subject(gdrive_auth_domain_wide_delegation)

    try:
        service = build('drive', 'v3', credentials=credentials)
        file_metadata = {'name': file_path, 'parents': [gdrive_folder_id]}
        media = MediaFileUpload(file_path, mimetype='application/sql')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        if file:
            file_id = file.get('id')
            print(f'File {file_path} uploaded to Google Drive with ID: {file_id}')
            return file_id
        else:
            print(f'Failed to upload {file_path} - no file object returned')
            return None

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    except Exception as error:
        print(f'An unexpected error occurred: {error}')
        return None

if __name__ == "__main__":
    required_env_vars = [
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'GDRIVE_FOLDER_ID',
        'GDRIVE_AUTH_KEY'
    ]
    env_vars = {}
    
    for var in required_env_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"The environment variable {var} is not set.")
        env_vars[var] = value
    
    db_name = env_vars['DB_NAME']
    db_user = env_vars['DB_USER']
    db_password = env_vars['DB_PASSWORD']
    db_host = env_vars['DB_HOST']
    db_port = env_vars.get('DB_PORT', 5432)
    gdrive_folder_id = env_vars['GDRIVE_FOLDER_ID']

    gdrive_auth_key = env_vars['GDRIVE_AUTH_KEY']
    gdrive_auth_key = gdrive_auth_key.strip("'")
    with open('credentials.json', 'w') as f:
        f.write(gdrive_auth_key)
    gdrive_auth_domain_wide_delegation = env_vars['GDRIVE_AUTH_DOMAIN_WIDE_DELEGATION']

    backup_file = backup_postgresql(db_name, db_user, db_password, db_host, db_port)
    upload_to_gdrive(backup_file, gdrive_folder_id, gdrive_auth_domain_wide_delegation)