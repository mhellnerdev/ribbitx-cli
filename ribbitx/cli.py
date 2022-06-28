import requests
import os
import subprocess
import click


base_uri = "https://ribbitx.jfrog.io/artifactory/api"
api_key = os.environ.get('JFROG_API_KEY')
headers = {"X-JFrog-Art-Api": api_key}


@click.group()
def cli():
  pass

@click.command()
def ping():
  click.echo('Pinging.... Response 200 means OK!')
  ping_response = requests.get(f"{base_uri}/system/ping", headers=headers)
  print(ping_response)

@click.command()
def version():
  click.echo('Getting remote instance version...')
  version_response = requests.get(f"{base_uri}/system/version", headers=headers)
  version_json = version_response.json()
  print("Artifactory Version: " + version_json['version'])

@click.command()
def storage():
  storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
  storage_json = storage_reponse.json()
  print(storage_json['fileStoreSummary'])

@click.command()
def listrepos():
  repo_type = input("What type of repositories would you like listed, REMOTE, LOCAL, or VIRTUAL? ")
  repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
  repo_json = repo_response.json()
  print(repo_json)


cli.add_command(ping)
cli.add_command(version)
cli.add_command(storage)
cli.add_command(listrepos)