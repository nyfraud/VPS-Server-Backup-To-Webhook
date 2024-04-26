import os
import zipfile
import requests
import time

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1233235678716756068/bY25Cmvw3v6WnKPG9jB0sdUtNrFNz3WOC-zMfPTyznOqj6l6z0m3PmmmbiWhhnDPAIBG"

# Directory to monitor
MONITORED_DIR = "/root/backup"

def get_files_in_directory(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def compile_files_into_zip(files):
    zip_file_name = "compiled_files.zip"
    zip_file_path = os.path.join(MONITORED_DIR, zip_file_name)
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for file_path in files:
            file_name = os.path.basename(file_path)
            zipf.write(file_path, arcname=file_name)
    return zip_file_path

def send_zip_to_discord(zip_file_path):
    try:
        with open(zip_file_path, "rb") as file:
            file_content = file.read()
        payload = {
            "content": "Compiled files",
            "file": ("compiled_files.zip", file_content)
        }
        response = requests.post(WEBHOOK_URL, files=payload)
        if response.status_code == 200:
            print("Zip file sent successfully")
        else:
            print(f"Failed to send zip file, HTTP {response.status_code}")
    except Exception as e:
        print(f"Error sending zip file: {e}")

def main():
    while True:
        files = get_files_in_directory(MONITORED_DIR)
        if files:
            zip_file_path = compile_files_into_zip(files)
            send_zip_to_discord(zip_file_path)
        time.sleep(30)  # Wait for 30 seconds before checking again

if __name__ == "__main__":
    main()
