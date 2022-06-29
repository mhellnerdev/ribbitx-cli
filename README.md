# ribbitx-cli

- Built on Python 3.8.10
- Link to Artifactory Artifact [https://ribbitx.jfrog.io/artifactory/ribbitx-pypi/](https://ribbitx.jfrog.io/artifactory/ribbitx-pypi/)

## Installing RibbitX as an executable script
- This can be installed as an executable script via pip. This allows for the simple running of command "ribbitx" to invoke from the command line.
- To install, run the following command from the root of the project folder and it will make use of the setup.py file to install as an executable script.
```
pip install .
```
- You may now simply run the command 'ribbitx' to invoke.

## Commands available
- ribbitx ping - This will do a status check on the JFrog Hosted instance by means of REST API HTTP Response. If you receive a Status 200, then your instance is up and available.
- ribbitx version - This will return the hosted version of Artifactory.
- ribbitx storage - This will return RAW JSON for the fileStoreSummary keys. This includes Total Space, Used Space, and Free Space of your instance.
- ribbitx getrepos - This will return a list of your repositories in RAW JSON. If you would like to filter by type, the cli tool will ask if you would like to view LOCAL, REMOTE, or VIRTUAL repos.


## Design Decisions
- This being my very first Python CLI application, I had to do some research on how to execute this. My first thought was to build a terminal menu system that I could pass curl commands via BASH scripts or Python subprocess libraries.
- Python3 was decided upon for writing the application. This would allow me to use some existing extensible frameworks for the CLI application. "Click" library was chosen due to it's easy to understand documentation.
- After reading JFrog's documentation on how to interact with the Artifactory SaaS Web API, the "Requests" librarty was chosen for the application.

## Sources
- Official Click Documentation [https://click.palletsprojects.com/en/8.1.x/](https://click.palletsprojects.com/en/8.1.x/) 
- Software Engineer Haydn's video guides helped immensely with getting me started with Click. [https://www.youtube.com/playlist?list=PLKvQZ5ahnOLQSNyEe2c9j4NCVGxIuw0Cp](https://www.youtube.com/playlist?list=PLKvQZ5ahnOLQSNyEe2c9j4NCVGxIuw0Cp)


### API KEY
 - [ommitted]