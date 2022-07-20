from encodings import search_function
import os
from xxlimited import new
import requests
import click
import json
import getpass
import traceback


# base api url
base_uri = "https://ribbitx.jfrog.io/artifactory/api"

# api key. with this method, the api key must be exported to your local OS environment variables as JFROG_API_KEY.
api_key = os.environ.get("JFROG_API_KEY")

# hardcoded api key
# api_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# headers variable that is passed into the request string
headers = {"X-JFrog-Art-Api": api_key}


# required to group below extensible commands
@click.group()
@click.version_option()
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
    click.secho(f"HTTP Response {status_code}", fg="green")
    
    if status_code == 200:
        click.secho("HTTP Status OK", fg="green")
    else:
        click.secho("Please check instance. Potentially Unhealthy.", fg="bright_red")


# version command to check version of hosted instance
@click.command("version", short_help="Check version of Artifactory instance.")
def version():
    """Checks version of Artifactory instance."""
    click.secho("Getting remote instance version...", fg="green")
    version_response = requests.get(f"{base_uri}/system/version", headers=headers)
    version_json = version_response.json()
    click.secho("Artifactory Version: " + version_json["version"])
    click.secho("Artifactory Revision: " + version_json["revision"])


# storage command to check status of hosted instance storage
@click.command("storage", short_help="Check Storage usage of Artifactory instance.")
def storage():
    """Check Storage usage of Artifactory instance."""
    storage_reponse = requests.get(f"{base_uri}/storageinfo", headers=headers)
    storage_json = storage_reponse.json()
    pretty_storage = json.dumps(storage_json["fileStoreSummary"], indent=4)
    click.secho(pretty_storage, fg="green")


# listrepos command to check list of available repos on the hosted instance
@click.command("repo-list", short_help="List repositories.")
def repolist():
    """List repositories."""
    repo_type = input(
        "What type of repositories would you like listed, local, remote, or virtual? ")
    repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
    repo_json = repo_response.json()

    for repo_name in repo_json:
      click.secho(repo_name["key"])


# create repository command
@click.command("repo-create", short_help="Create a new repository.")
def repocreate():
    """Create a new repository."""
    click.secho("This command will CREATE a new local repository!", fg="green")
    repo_name = input("Please enter new repository name: ")
    repo_type = input("Please enter repository type: (local, remote, virtual): ")
    package_type = input("Please enter the package type of this repository: ")
    repo_description = input("Please enter the public description: ")
    repo = { "key": repo_name, "rclass": repo_type, "packageType": package_type, "description": repo_description }
    
    try:
      repocreate_request = requests.put(f"{base_uri}/repositories/" + repo["key"], json=repo, headers=headers)
      repocreate_status = repocreate_request.status_code
      repocreate_content = repocreate_request.content

      if repocreate_status == 200:
        click.secho(f"Successfully created repository '{repo_name}'", fg="green")
      else:
        try:  
          repocreate_json = repocreate_request.json()
          repocreate_error = repocreate_json["errors"]
          repocreate_message = repocreate_error[0]
          click.secho("There was an Error. See below:", fg="bright_red")
          click.secho(repocreate_message["message"], fg="yellow")
        except:
          click.echo("There was an undefined error!")
    except:
      click.secho("There has been an exception error.", fg="bright_red")


# update repository description command
@click.command("repo-update", short_help="Update a repository's public description.")
def repoupdate():
    """Update a repository description."""
    click.secho("This command will allow you to update the public description of a selected local repository.", fg="green")
    repo_name = input("Please enter the repository name you are updating: ")
    repo_description = input("Enter the new description: ")
    repo = { "key": repo_name, "description": repo_description }
    repoupdate_request = requests.post(f"{base_uri}/repositories/" + repo["key"], json=repo, headers=headers)
    repoupdate_status = repoupdate_request.status_code
    repoupdate_content = repoupdate_request.content
    repoupdate_json = repoupdate_request.json
    
    if repoupdate_status == 200:
      click.secho("The repo public description has been updated!", fg="green")
    else:
      click.secho("There was an error. Repository not updated.", fg="bright_red")


# delete repository command
# TODO work on error handling for this command
@click.command("repo-delete", short_help="Delete a repository.")
def repodelete():
  """Delete a repository."""
  click.secho("This command will DELETE a selected repository!", fg="bright_red", bold=True)
  repo_type = input("What type of repository would you like to DELETE? (local, remote, or virtual) ")

  # get repository list
  repo_response = requests.get(f"{base_uri}/repositories?type={repo_type}", headers=headers)
  repo_json = repo_response.json()
  # loop through repo list json
  for repo_name in repo_json:
    click.secho(repo_name["key"])

  click.secho("This command will DELETE a selected repository!", fg="bright_red", bold=True)
  repo_to_delete = input("What is the name of the repository you wish to delete: ")
  click.secho(f"Are you sure you want to delete the repository named: {repo_to_delete} [y/n] ", fg="yellow", bold=True, nl=False)
  delete_repo = click.getchar()
  delete_answer = delete_repo.lower()
  click.echo()
  
  try:
    if delete_answer == "y":
      deleterepo_request = requests.delete(f"{base_uri}/repositories/{repo_to_delete}", headers=headers)
      deleterepo_status = deleterepo_request.status_code
    elif delete_answer == "n":
      click.secho("Deletion Canceled", fg="bright_red")
      exit()
    else:
      click.echo("Invalid Input. Try again.")
  except Exception as e:
    click.secho("There has been an exception error!", fg="bright_red")
    traceback.print_exc() # used for debugging
    click.secho(e)
  
  if deleterepo_status == 200:
    click.secho(f"The repository: {repo_to_delete} has been removed successfully.", fg="green")
  elif deleterepo_status == 401:
    click.secho(f"You are not authorized to delete user {repo_to_delete}", fg="bright_red")
  elif deleterepo_status == 404:
    click.secho(f"Error: Repository {repo_to_delete} not found.", fg="bright_red")
  else:
    click.secho("Error: Repository not deleted.", fg="bright_red")


# list users command
@click.command("user-list", short_help="List users of your instance.")
def userlist():
  """List users of your instance"""
  userlist_response = requests.get(f"{base_uri}/security/users", headers=headers)
  userlist_status = userlist_response.status_code
  userlist_content = userlist_response.content
  userlist_json = userlist_response.json()
  userlist_dict = json.loads(userlist_response.text)
 
  for username in userlist_dict:
    click.secho(username["name"])


# create a new user command
@click.command("user-create", short_help="Create a new user.")
def usercreate():
  """Create a new user."""
  new_username = input("Please enter new username: ")
  new_user_email = input("Please enter new user's email address: ")
  new_user_password = getpass.getpass("Enter Password: ", stream=None)
  user_info = { "name": new_username, "email": new_user_email, "password": new_user_password }
  new_user_response = requests.put(f"{base_uri}/security/users/" + user_info["name"], json=user_info, headers=headers)
  new_user_status = new_user_response.status_code
  
  try:
    try:
      if new_user_status == 201:
        click.secho(f"The user: {new_username} has been created.", fg="green")
      elif new_user_status == 400:
        new_user_content = new_user_response.content
        click.secho("There was an Error 400. See below:", fg="bright_red")
        new_user_json = json.loads(new_user_content)        
        click.secho(new_user_json["errors"][0]["message"], fg="yellow")
      else:
        click.secho("There was an Undefined Error. See below:", fg="bright_red")
        click.secho(new_user_response)
        click.secho(new_user_content)        
    except Exception as e:
      click.secho("There was an exception error!", fg="bright_red")
      traceback.print_exc() # used for debugging
      click.echo(e)    
  except Exception as e:
    click.secho("There has been an exception error!", fg="bright_red")
    traceback.print_exc() # used for debugging
    click.secho(e)


# delete user command
@click.command("user-delete", short_help="Delete a user.")
def userdelete():
  """Delete a user."""
  click.secho("This command will DELETE a selected user!", fg="bright_red", bold=True)
  
  # get user list and store in json
  userlist_response = requests.get(f"{base_uri}/security/users", headers=headers)
  userlist_dict = json.loads(userlist_response.text)
  # loop through json list of users
  for username in userlist_dict:
    click.secho(username["name"])
  
  username = input("What is the username you wish to delete: ")
  click.secho(f"Are you sure you want to delete {username}'s account? [y/n] ", fg="yellow", nl=False)
  delete_user = click.getchar(echo=True)
  delete_answer = delete_user.lower()
  click.echo()  

  try:
    if delete_answer == 'y':    
      deleteuser_request = requests.delete(f"{base_uri}/security/users/{username}", headers=headers)
      deleteuser_status = deleteuser_request.status_code
    elif delete_answer == 'n':
      click.secho("Deletion Canceled.", fg="bright_red")
      exit()
    else:
      click.secho("Invalid Input. Try again.", fg="yellow")
      exit()
  except Exception as e:
    click.secho("There has been an exception error!")
    traceback.print_exc() # used for debugging
    click.secho(e)    
  
  if deleteuser_status == 200:
    click.secho(f"The user: {username} has been deleted successfully.", fg="green")
  elif deleteuser_status == 401:
    click.secho(f"You are not authorized to delete user {username}", fg="bright_red")
  elif deleteuser_status == 404:
    click.secho(f"Error: User {username} not found.", fg="bright_red")
  else:
    click.secho("Error: User not deleted.", fg="bright_red")


# add functions available to be called as commands
cli.add_command(ping)
cli.add_command(version)
cli.add_command(storage)
cli.add_command(repolist)
cli.add_command(repocreate)
cli.add_command(repoupdate)
cli.add_command(repodelete)
cli.add_command(userlist)
cli.add_command(usercreate)
cli.add_command(userdelete)

