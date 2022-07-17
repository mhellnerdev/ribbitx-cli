import os
import requests
import click
import json
import getpass


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


# command makes use of API ping to check HTTP status of hosted instance
@click.command("ping", short_help="Checks HTTP status of your Artifactory instance.")
def ping():
    """Checks HTTP and ping status of your Artifactory instance."""
    click.echo("Pinging.... Response 200 means OK!")
    ping_response = requests.get(f"{base_uri}/system/ping", headers=headers)
    status_code = ping_response.status_code
    http_status = str(ping_response.content)
    click.echo(click.style(f"HTTP Response {status_code}", fg="green"))
    if status_code == 200:
        click.echo(click.style("HTTP Status OK", fg="green"))
    else:
        click.echo(click.style("Please check instance. Potentially Unhealthy.", fg="red"))


# version command to check version of hosted instance
@click.command("version", short_help="Check version of Artifactory instance.")
def version():
    """Checks version of Artifactory instance."""
    click.echo(click.style("Getting remote instance version...", fg="green"))
    version_response = requests.get(f"{base_uri}/system/version", headers=headers)
    version_json = version_response.json()
    click.echo("Artifactory Version: " + version_json["version"])
    click.echo("Artifactory Revision: " + version_json["revision"])


# storage command to check status of hosted instance storage
@click.command("storage", short_help="Check Storage usage of Artifactory instance.")
def storage():
    """Check Storage usage of Artifactory instance."""
    storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
    storage_json = storage_reponse.json()
    pretty_storage = json.dumps(storage_json["fileStoreSummary"], indent=4)
    click.echo(pretty_storage)


# listrepos command to check list of available repos on the hosted instance
@click.command("repo-list", short_help="List repositories.")
def repolist():
    """List repositories."""
    repo_type = input(
        "What type of repositories would you like listed, local, remote, or virtual? ")
    repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
    repo_json = repo_response.json()
    pretty_repos = json.dumps(repo_json, indent=4)
    # click.echo(pretty_repos)
    click.echo(repo_response.content)


# create repository command
@click.command("repo-create", short_help="Create a new repository.")
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
      click.echo(click.style(f"Successfully created repository '{repo_name}'", fg="green"))
    elif repocreate_status == 409:
      click.echo(click.style("409 Error: An invalid character is being used.", fg="bright_red"))
    else:
      click.echo(repocreate_request.content)


# update repository description command
@click.command("repo-update", short_help="Update a repository's public description.")
def repoupdate():
    """Update a repository description."""
    click.echo(click.style("This tool will allow you to update the public description of a selected local repository.", fg="green"))
    repo_name = input("Please enter the repository name you are updating: ")
    repo_description = input("Enter the new description: ")
    repo = { "key": repo_name, "description": repo_description }
    repoupdate_request = requests.post(f"{base_uri}/repositories/" + repo["key"], json=repo, headers=headers)
    repoupdate_status = repoupdate_request.status_code
    if repoupdate_status == 200:
      click.echo(click.style("The repo public description has been updated!", fg="green"))
    else:
      click.echo(click.style("There was an error. Repository not updated.", fg="bright_red"))

  
# create a new user command
@click.command("user-create", short_help="Create a new user.")
def usercreate():
  """Create a new user."""
  new_username = input("Please enter new username: ")
  new_user_email = input("Please enter new user's email address: ")
  new_user_password = getpass.getpass("Enter Password: ", stream=None)
  user_info = { "name": new_username, "email": new_user_email, "password": new_user_password }
  new_user_request = requests.put(f"{base_uri}/security/users/" + user_info["name"], json=user_info, headers=headers)
  new_user_status = new_user_request.status_code
  if new_user_status == 201:
    click.echo(click.style(f"The user: {new_username} has been created.", fg="green"))
  else:
    click.echo(click.style("There has been an error. Please make sure email address is correct or try a stronger password.", fg="bright_red"))


# delete user command
@click.command("user-delete", short_help="Delete a user.")
def userdelete():
    """Delete a user."""
    username = input("What is the username you wish to delete: ")
    click.echo(click.style(f"Are you sure you want to delete {username}'s account? [y/n] ", fg="yellow"))
    delete_user = click.getchar()
    click.echo()
    if delete_user == "y":
      deleteuser_request = requests.delete(f"{base_uri}/security/users/{username}", headers=headers)
    elif delete_user == "n":
      click.echo(click.style("Deletion Canceled", fg="bright_red"))
      exit()
    else:
      click.echo("Invalid Input. Try again.")

    deleteuser_status = (deleteuser_request.status_code)
    
    if deleteuser_status == 200:
      click.echo(click.style(f"The user: {username} has been removed successfully.", fg="green"))
    elif deleteuser_status == 401:
      click.echo(click.style(f"You are not authorized to delete user {username}", fg="bright_red"))
    elif deleteuser_status == 404:
      click.echo(click.style(f"Error: User {username} not found.", fg="bright_red"))
    else:
      click.echo(click.style("Error: User not deleted.", fg="bright_red"))

    




# add functions available to be called as commands
cli.add_command(ping)
cli.add_command(version)
cli.add_command(storage)
cli.add_command(repolist)
cli.add_command(repocreate)
cli.add_command(repoupdate)
cli.add_command(usercreate)
cli.add_command(userdelete)
