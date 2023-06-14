# FastAPI API template
This is an example of how to dockerize a python FastAPI REST API with auth.

This is an example python project to demonstate the following points:
- [x] python project structure example suitable for most projects
- [x] pytest and TDD (Test Driven Development)
- [ ] containerization
- [x] use of python best practices (PEP8)
- [x] pylint
- [ ] use of pre-commits

This demo contains a REST API built over FastAPI, this repository can be used as a starting point for other projects too and not only REST API. 

## Before you start
Make sure docker, pyenv and pipenv are installed, if you need any of this tools refer to the following sources:
- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://github.com/pypa/pipenv#installation) or, if you are using MacOS you can also refer to this [link](https://formulae.brew.sh/formula/pipenv)
- [docker](https://docs.docker.com/engine/install/), if you are using Windows i suggest the use of WSL and installation via WSL engine

## Development
This section presents the development workflow and tools to work with this repository.

**!!!IMPORTANT!!!**
Move inside the directory where this README is located to execute all of the commands in this README.md
```shell
$ cd %path-to-the-repository%/fastapi
```

### Project structure
```shell
.
├── .env.example
├── configs
├── dockerfiles
├── scripts
├── src
├── tests
├── Pipfile
├── Pipfile.lock
├── README.md
└── pyproject.toml
```

* `configs` contains configuration files for the application in order to run properly.
* `dockerfiles` contains all the required dockerfiles (if there are any)
* `scripts` contains some scripts (if there are any) that can run within pipenv or that can be run with the shell (no rules here)
* `src` contains the application package (documentation is provided with the use of docstrings inside of the code)
* `tests` contains the test package to run with pytest
* `Pipfile` and `Pipfile.lock` are files used by pipenv to manage the project and virtualenv
* `pyproject.toml` is a file used to describe the python project and create the editable module to be tested or the actual module to be released to the public if required



### Prepare a local environment
To prepare the development environment some steps are required, open your favourite terminal and execute the following commands:
1. return the latest python 3.10 version and store it to an environment variable
```shell
$ pyenv install --list | grep -E "\s3\.10\.[0-9]+" -o | sort -nrk 3 -t . | head -n 1 | read PYENV_TO_INSTALL
```

2. install the latest python 3.10 version
```shell
$ pyenv install -s $PYENV_TO_INSTALL
```

3. activate the installed python version
```shell
$ pyenv local $PYENV_TO_INSTALL
```

4. unset the generated environment variable
```shell
$ unset PYENV_TO_INSTALL
```

4. it is now time to create the virtualenv with pipenv
```shell
$ pipenv install -d
```

At this point if the execution ran succesfuly to check the virtualenv is correctly installed type
```shell
$ pipenv run pip list
```
and as return value you should see the installed modules for the virtualenv installed, its path can be retrieved by typing
```shell
$ pipenv --venv
```

you can now open this folder in your preferred IDE/Text Editor and use the output of the last command to tell the IDE/Text Editor the correct interpreter and have hints while you type.

### Startup the application
To startup this application a MongoDB instance and a dotenv file are required, we are proceeding to generate them right now.
First of all the dotenv file can be created starting by the provided `.env.example` with
```shell
$ cp .env.example .env
```
at this point is required to change some of the environment variables in it:
* `SECRET_KEY` to sign the JWT in use which can be generated with
```shell
$ openssl rand -hex 32
```
* `LOGGING_DIR` to store the application logs can be whatever absolute path in your machine, up to you.
* `CONFIGS_DIR` must be replaced with the result of
```shell
$ echo $(pwd)/configs
```
* Variables starting with `DB_` are used to execute the connection to the MongoDB instance, do not modify.

At this point you can start the application:
1. Start the MongoDB instance, follow the described steps in [here](../mongo/README.md)

2. Use a script that has been added to the Pipfile typing
```shell
$ pipenv run serve-dev
```

After the server started you can access to the [swagger](http://localhost:8000/docs) or [redoc](http://localhost:8000/redoc) documentation to try the provided API.

Alternatively if you are using an IDE/Text Editor that supports visual breakpoints you can start it from there to have some more information about the debug. For Visual Studio Code in the debug configuration you can add a new configuration for python programs, then a new menu is displayed where to chose the "FastAPI" application. A json file will be displayed, insert the following body, if required adapt it
```json
{
    "name": "Python: FastAPI",
    "type": "python",
    "request": "launch",
    "module": "uvicorn",
    "args": [
        "src.app:fastapi_app",
        "--reload"
    ],
    "jinja": true,
    "justMyCode": true,
    "envFile": "${workspaceFolder}/.env"
}
```

## Testing
To include unit tests pytest is used, more information on its usage is available [here](https://docs.pytest.org/en/7.3.x/)


Two scripts for testing are included in this project with `Pipfile`:
* List only the tests
```shell
$ pipenv run tests-list
```

* Run the tests
```shell
$ pipenv run tests
```
A `dotenv` for test is required under `./env/.env.test`, the configuration for pytest is included in `pyproject.toml` under the [tool.pytest.ini_options] table. You can change it to use whatever environemnt file you prefer. Just remember a running MongoDB instance is required to launch the tests.

## Formatting and linting
To make more readable code black, black and isort are provided as dependencies for development alongside with custom Pipfile scripts (open Pipefile to see 'em).
Format the code by typing in your terminal from this python project repository:
```shell
$ pipenv run format-code
$ pipenv run format-import
```

After cleaning the code out from human inconsistencies you can run the following command to score your code and see where it can require improvments:
```shell
$ pipenv run check-syntax
```
Settings for pylint are provided in the `pylintrc` file.
# Docker
For development the dockerization has been removed since pipenv provides all the required features I was searching for when upgrading to it. In future this section will be populated to add informations to deploy in a production environment.
