# ribbitx-cli

- Built on Python 3.8.10

## Installing Package as an executable script
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
- ribbitx getrepos - This will return a list of your repositories. If you would like to filter by type, the cli tool will ask if you would like to view LOCAL, REMOTE, or VIRTUAL repos.