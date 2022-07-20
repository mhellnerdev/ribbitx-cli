# ribbitx-cli

- Built on Python 3.8.10
- Link to Artifactory Artifact [https://ribbitx.jfrog.io/artifactory/ribbitx-pypi/](https://ribbitx.jfrog.io/artifactory/ribbitx-pypi/)
- 10 API's used. GET, POST, PUT, DELETE methods for managing your SaaS instance of JFROG Artifactory.

### Version 0.50 Updates - Major Update
- Added user-list command.
- The user-list prints to console when running user-delete.
- The repo-list command now prints a more readable list to the console. The json is now looping through and outputting a cleaner formatted list.
- The repo-list now prints to the console when running repo-delete.
- Error Handling added. When a command fails, the JSON response error key is printed to the console or an exception is thrown.
- Error handling is now working for create-repo, update repo, delete-repo, user-create, and user-delete.
- Case-sensitivity is no longer an issue when given a "y/n" prompt.

### Version 0.4 Updates
- Error handling is now working for repo-create command.
- added ribbitx --version feature.

### Version 0.3 Updates
- Added color styles to command line prompts.
- Improved prompts. Now asks Y/N for deletion prompts.
- Added repo-delete feature.
- Added ability to enter description for create-repo command.

### Version 0.2 Updates
- Changed commands to prefix with repo or user depending on action being taken.
- Added repo-create, repo-update, user-create, user-delete features. PUT, POST, and DELETE methods used.
- Pruned requirements file.
- Formatted JSON output for repo-list and storage commands.

## Installing RibbitX as an executable script
- This can be installed as an executable script via pip. This allows for the simple running of command "ribbitx" to invoke from the command line.
- To install, run the following command from the root of the project folder and it will make use of the setup.py file to install as an executable script.
```
pip install --editable .
```
- You may now simply run the command '**ribbitx**' to invoke.

## Commands available
- **ribbitx ping** - This will do a status check on the JFrog Hosted instance by means of REST API HTTP Response. If you receive a Status 200, then your instance is up and available.
- **ribbitx version** - This will return the hosted version of Artifactory.
- **ribbitx storage** - This will return formatted JSON for the fileStoreSummary keys. This includes Total Space, Used Space, and Free Space of your instance.
- **ribbitx repo-list** - This will return a list of your repositories in formatted JSON. If you would like to filter by type, the cli tool will ask if you would like to view LOCAL, REMOTE, or VIRTUAL repos.
- **ribbitx repo-create** - This will create a new repository and exposes options to name the repository, choose local, remote, or virtual, and choose package type.
- **ribbitx repo-delete** - This will allow you to delete a local repository by entering name.
- **ribbitx repo-update** - This will allow you to update the public description of a local repository.
- **ribbitx user-list** - This will allow you to list all users with accounts on your instance.
- **ribbitx user-create** - This will allow for creating new users with zero permissions. You are able to set username, email, and password.
- **ribbitx user-delete** - This will allow you to delete a user account on your instance.


## Design Decisions
- This being my very first Python CLI application, I had to do some research on how to execute this. My first thought was to build a terminal menu system that I could pass curl commands via BASH scripts or Python subprocess libraries.
- Python3 was decided upon for writing the application. This would allow me to use some existing extensible frameworks for the CLI application. "Click" library was chosen due to it's easy to understand documentation.
- After reading JFrog's documentation on how to interact with the Artifactory SaaS Web API, the "Requests" library was chosen for the application.

## Sources
- Official JFROG Artifactory documentation - [https://jfrog.com/confluence/display/JFROG/Artifactory+REST+API](https://jfrog.com/confluence/display/JFROG/Artifactory+REST+API)
- Official Click Documentation [https://click.palletsprojects.com/en/8.1.x/](https://click.palletsprojects.com/en/8.1.x/) 
- Software Engineer Haydn's video guides helped immensely with getting me started with Click. [https://www.youtube.com/playlist?list=PLKvQZ5ahnOLQSNyEe2c9j4NCVGxIuw0Cp](https://www.youtube.com/playlist?list=PLKvQZ5ahnOLQSNyEe2c9j4NCVGxIuw0Cp)
