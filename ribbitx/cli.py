import requests
import os
import click


# base api url
base_uri = "https://ribbitx.jfrog.io/artifactory/api"

# api key. with this method, the api key must be exported to your local OS environment variables as JFROG_API_KEY.
api_key = os.environ.get('JFROG_API_KEY')

# hardcoded API KEY
# api_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# headers variable that is passed into the request string
headers = {"X-JFrog-Art-Api": api_key}

# required to group below extensible commands
@click.group()
def cli():
  """
    Welcome to the RibbitX CLI tool.

    This tool was authored to assist in the management of your
    Cloud Hosted Artifactory Instance.

    Usage is listed in the commands section below.    
  """

# ping command to check HTTP status of hosted instance
@click.command('ping', short_help='Checks HTTP status of your Artifactory instance.')
def ping():
  """Checks HTTP and ping status of your Artifactory instance."""
  click.echo('Pinging.... Response 200 means OK!')
  ping_response = requests.get(f"{base_uri}/system/ping", headers=headers)
  print(ping_response)

# version command to check version of hosted instance
@click.command('version', short_help='Check version of Artifactory instance.')
def version():
  """Checks version of Artifactory instance."""
  click.echo('Getting remote instance version...')
  version_response = requests.get(f"{base_uri}/system/version", headers=headers)
  version_json = version_response.json()
  print("Artifactory Version: " + version_json['version'])

# storage command to check status of hosted instance storage
@click.command('storage', short_help='Check Storage usage of Artifactory instance.')
def storage():
  """Check Storage usage of Artifactory instance."""
  storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
  storage_json = storage_reponse.json()
  print(storage_json['fileStoreSummary'])

# listrepos command to check list of available repos on the hosted instance
@click.command('listrepos', short_help='List repos.')
def listrepos():
  """List repos."""
  repo_type = input("What type of repositories would you like listed, REMOTE, LOCAL, or VIRTUAL? ")
  repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
  repo_json = repo_response.json()
  print(repo_json)


# add functions available to be called as commands
cli.add_command(ping)
cli.add_command(version)
cli.add_command(storage)
cli.add_command(listrepos)