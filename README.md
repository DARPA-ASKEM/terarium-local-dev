# Terarium Local Development
A repository to run local development.

## Setup
1. Run `python3 -m virtualenv venv` to set up the virtual env.
2. Run `source venv/bin/activate` to enter the virtual environment.
3. Run `pip install -r requirements.txt` to install the builder requirements.


## The Builder Command
```
usage: builder.py [-h] [-e ENV] [-d DEFAULTS] [-l LOCAL] [-s STAGING] [-x EXTRACT]

options:
  -h, --help            show this help message and exit
  -e ENV, --env ENV     Custom env file to write out.
  -d DEFAULTS, --defaults DEFAULTS
                        Flag that sets up the build to use default ENV values.
  -l LOCAL, --local LOCAL
                        Flag that sets up the build as full local install. -- Not Implemented
  -s STAGING, --staging STAGING
                        Flag that sets up the job as a staging install. -- Not Implemented
  -x EXTRACT, --extract EXTRACT
                        Flag that sets up the job as an extraction to write new services to the components
                        directory. -- Not Implemented
```

## Quickstart
To get the service up and running, you can simply run `python builder.py -d true`.  This will walk you through
the service setup and use the initial ENV values from `services.json` to set up the service.

## Complete ENV Set Up
If you want to configure your service completely you can run `python builder.py`.  This will walk you through
setting up every pertinent environment variable for every enabled service.

## Service Files
The docker compose file is built using the yaml files in the `components` directory.  You can review these files
to understand the ENV values and what they map to in the service definition.

## Building a Local Service
If you want to build a service from your local repository you can achieve this by running the builder 
(`python builder.py`) and select `y` when prompted for a local build.  You will need to supply the 
absolute path to the repository via the build prompt or by adding `build_paths.json` file with the
service listed. 

    {
        "data-service": "/path/to/data-service-repo",
        "hmi-client": "/path/to/Terarium",
        "hmi-server": "/path/to/Terarium",
        "simulation-service": "/path/to/simulation-service",
        "pyciemss_api": "/path/to/pyciemss-service"
    }

This file will automatically supply the build path to enable a local build.
