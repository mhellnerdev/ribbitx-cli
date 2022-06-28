import requests
import os
import subprocess

base_uri = "https://ribbitx.jfrog.io/artifactory/api"
api_key = os.environ.get('JFROG_API_KEY')
headers = {"X-JFrog-Art-Api": api_key}

# GET Ping/Status Response
ping_response = requests.get(f"{base_uri}/system/ping", headers=headers)
print(ping_response)

# GET Version Info
version_response = requests.get(f"{base_uri}/system/version", headers=headers)
version_json = version_response.json()
print("Artifactory Version: " + version_json['version'])

# GET Storage Info
storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
storage_json = storage_reponse.json()
print(storage_json['fileStoreSummary'])

# GET Repository List
repo_type = input("What type of repositories would you like listed, REMOTE, LOCAL, or VIRTUAL? ")
repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
repo_json = repo_response.json()
print(repo_json)

# # Create New User
# user_name = input("Creating New User. Please enter the username: ")
# requests.put(f"{base_uri}/security/users/{user_name}", headers=headers)

