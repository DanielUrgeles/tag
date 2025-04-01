import os
import requests
from datetime import datetime

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO_OWNER = "TU_USUARIO"
REPO_NAME = "Random_C"
TAG_NAME = datetime.now().strftime("%Y%m%d%H%M%S")
RELEASE_NAME = f"Release {TAG_NAME}"
EXE_FILE = "random"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Crear una release
release_data = {
    "tag_name": TAG_NAME,
    "name": RELEASE_NAME,
    "body": "Publicació automàtica de release",
    "draft": False,
    "prerelease": False
}

release_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
response = requests.post(release_url, json=release_data, headers=headers)

if response.status_code == 201:
    upload_url = response.json()["upload_url"].split("{")[0]
    with open(EXE_FILE, "rb") as f:
        files = {'file': (EXE_FILE, f, 'application/octet-stream')}
        upload_response = requests.post(upload_url + "?name=random", headers=headers, files=files)

        if upload_response.status_code == 201:
            print("✅ Release publicada amb èxit!")
        else:
            print("❌ Error pujant l'executable:", upload_response.json())
else:
    print("❌ Error creant la release:", response.json())
