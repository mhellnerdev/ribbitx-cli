import requests
import os
import click
import json


# base api url
base_uri = "https://ribbitx.jfrog.io/artifactory/api"

# api key. with this method, the api key must be exported to your local OS environment variables as JFROG_API_KEY.
api_key = os.environ.get("JFROG_API_KEY")

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


# use of API ping to check HTTP status of hosted instance
@click.command("ping", short_help="Checks HTTP status of your Artifactory instance.")
def ping():
    """Checks HTTP and ping status of your Artifactory instance."""
    click.echo("Pinging.... Response 200 means OK!")
    ping_response = requests.get(f"{base_uri}/system/ping", headers=headers)
    status_code = ping_response.status_code
    http_status = str(ping_response.content)
    click.echo(f"HTTP Response {status_code}")
    if status_code == 200:
        click.echo("HTTP Status OK")
    else:
        click.echo("Please check instance. Potentially Unhealthy.")


# version command to check version of hosted instance
@click.command("version", short_help="Check version of Artifactory instance.")
def version():
    """Checks version of Artifactory instance."""
    click.echo("Getting remote instance version...")
    version_response = requests.get(f"{base_uri}/system/version", headers=headers)
    version_json = version_response.json()
    click.echo("Artifactory Version: " + version_json["version"])
    click.echo(version_response.content)


# storage command to check status of hosted instance storage
@click.command("storage", short_help="Check Storage usage of Artifactory instance.")
def storage():
    """Check Storage usage of Artifactory instance."""
    storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
    storage_json = storage_reponse.json()
    pretty_storage = json.dumps(storage_json["fileStoreSummary"], indent=4)
    click.echo(pretty_storage)


# listrepos command to check list of available repos on the hosted instance
@click.command("listrepos", short_help="List repos.")
def listrepos():
    """List repos."""
    repo_type = input(
        "What type of repositories would you like listed, LOCAL, REMOTE, or VIRTUAL? ")
    repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
    repo_json = repo_response.json()
    pretty_repos = json.dumps(repo_json, indent=4)
    # click.echo(pretty_repos)
    click.echo(repo_response.content)


# create repository command
@click.command("repocreate", short_help="Create a new repository.")
def repocreate():
    """Create a new repository."""
    repo_name = input("Please enter repo name: ")
    repo_type = input("Please enter repository type: (local, remote, virtual): ")
    package_type = input("Please enter the package type of this repo: ")
    repo = { "key": repo_name, "rclass": repo_type, "packageType": package_type }
    repocreate_request = requests.put(f"{base_uri}/repositories/" + repo["key"], json=repo, headers=headers)
    repocreate_status = repocreate_request.status_code
    repocreate_json = repocreate_request.json
    if repocreate_status == 200:
          click.echo(repocreate_request.content)
    else:
      # print(repocreate_json["errors"]["message"])
      click.echo(repocreate_request.content)



# update repository description commands
@click.command("repoupdate", short_help="Update a repository's public description.")
def repoupdate():
    """Update a repository description."""
    click.echo("This tool will allow you to update the public description of a selected repository.")
    repo_name = input("Please enter the repository name you are updating: ")
    repo_description = input("Enter the new description: ")
    repo = { "key": repo_name, "description": repo_description }
    repoupdate_request = requests.post(f"{base_uri}/repositories/" + repo["key"], json=repo, headers=headers)
    repoupdate_status = repoupdate_request.status_code
    if repoupdate_status == 200:
      click.echo("The repoo description public has been updated!")
    else:
      click.echo("There was an error. Repository not updated.")


# delete user command
@click.command("deleteuser", short_help="Delete user.")
def deleteuser():
    """Delete user."""
    username = input("What is the username: ")
    deleteuser_request = requests.delete(f"{base_uri}/security/users/{username}", headers=headers)
    deleteuser_status = (deleteuser_request.status_code)
    if deleteuser_status == 200:
      click.echo(f"{username} deleted!")
      click.echo(deleteuser_request.content)
    elif deleteuser_status == 401:
      click.echo(f"You are not authorized to delete user {username}")
    elif deleteuser_status == 404:
      click.echo(f"User {username} not found.")
    else:
      click.echo("User not deleted.")




# add functions available to be called as commands
cli.add_command(ping)
cli.add_command(version)
cli.add_command(storage)
cli.add_command(listrepos)
cli.add_command(repocreate)
cli.add_command(deleteuser)
cli.add_command(repoupdate)
