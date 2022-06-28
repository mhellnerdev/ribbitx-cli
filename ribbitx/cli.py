import requests
import os
import click


# base api url
base_uri = "https://ribbitx.jfrog.io/artifactory/api"

# api key. with this method, the api key must be exported to your local OS environment variables.
api_key = os.environ.get('JFROG_API_KEY')

# headers variable that is passed into the request string
headers = {"X-JFrog-Art-Api": api_key}

# required to group below extensible commands
@click.group()
def cli():
  pass

# ping command to check HTTP status of hosted instance
@click.command()
def ping():
  click.echo('Pinging.... Response 200 means OK!')
  ping_response = requests.get(f"{base_uri}/system/ping", headers=headers)
  print(ping_response)

# version command to check version of hosted instance
@click.command()
def version():
  click.echo('Getting remote instance version...')
  version_response = requests.get(f"{base_uri}/system/version", headers=headers)
  version_json = version_response.json()
  print("Artifactory Version: " + version_json['version'])

# storage command to check status of hosted instance storage
@click.command()
def storage():
  storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
  storage_json = storage_reponse.json()
  print(storage_json['fileStoreSummary'])

# listrepos command to check list of available repos on the hosted instance
@click.command()
def listrepos():
  repo_type = input("What type of repositories would you like listed, REMOTE, LOCAL, or VIRTUAL? ")
  repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
  repo_json = repo_response.json()
  print(repo_json)


# add functions available to be called as commands
cli.add_command(ping)
cli.add_command(version)
cli.add_command(storage)
cli.add_command(listrepos)