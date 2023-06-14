# FastAPI API tempalte
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
Make sure docker, pyenv and pipenv are installed, if you need any of this tools reefer to the following sources:
- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://github.com/pypa/pipenv#installation) or, if you are usign MacOS you can also reefer to this [link](https://formulae.brew.sh/formula/pipenv)
- [docker](https://docs.docker.com/engine/install/), if you are a Windows i suggest the use of WSL and installation via WSL engine

## Development
This section presents the development workflow and tools to work with this repository.

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
* `dockerfiles` contains all the requried dockerfiles (if there is any)
* `scripts` contains some scripts (if there is any) that can run within pipenv or that can be run with the shell (no rules here)
* `src` contains the application package (documentation is provided with the use of docstrings inside of the code)
* `tests` contains the test package to run with pytest
* `Pipfile` and `Pipfile.lock` are files used by pipenv to manage the project and virtualenv
* `pyproject.toml` is a file used to describe the python project and create the editable module to be tested or the actual module to be released to the public if required

### Prepare a local environment
To prepare the development environment some steps are required, open your favourite terminal and execute the following commands:
1. search the latest 3.10 available python version
```shell
$ pyenv install --list | grep "3.10."
```

2. install the latest python version python 3.10 
```shell
# replace the x with the latest fix number available
$ pyenv isntall 3.10.x
```

3. set the local python version to use the one you have just installed
```shell
# replace the x with the latest fix number available
$ pyenv local 3.10.x
```
this is going to create a file `.python-version`, this will be ignored because it has been included into the `.gitignore`

4. it is now time to create the virtualenv with pipenv
```shell
$ pipenv install -d
```
doing this will install all of the required dependencies for the develoment environment. In alternative to install the production dependencies simply type
```shell
$ pipenv install
```

At this point if the execution ran succesfuly to check the virtualenv is correctly installed type
```shell
$ pienv run pip list
```
and as retur value you should see the installed modules for the virtualenv installed, its path can be retrived by typing
```shell
$ pipenv --venv
```

you can now open this folder in your preferred IDE/Text Editor and use the output of the last command to tell the IDE/Text Editor the correct interpreter and have hints while you type.

### Startup the application
To startup this application a DB and a dotenv file are required, we are proceding to generate them right now.
First of all the dotenv file can be created starting by the provided `.env.example` with
```shell
$ cp .env.example .env
```
at this point is required to change some of the environment variables:
* `SECRET_KEY` which can be generated with
```shell
$ openssl rand -hex 32
```
* `LOGGING_DIR` and `CONFIGS_DIR` can be whatever absolute path in your machine, up to you.
* If you already have a running instance of mongo to connect just use that (you can find and example of collection the API uses inside `../mongo/docker-entrypoint-intdb.d/mongo-init.js` script). Otherwise if you need one follow [this](../mongo/README.md) guide. When using the second option make sure to chanhge `DB_HOST=host.docker.internal`

At this point you have 2 options to start a local server:
1. Use a script that has been added to the Pipfile typing
```shell
$ pipenv run serve-dev
```
2. If you are using an IDE/Text Editor that supports visual breakpoints you can start it from there to have some more information about the debug. For Visual Studio Code in the debug configuration you can add a new configuration for python programs, then a new menu is displayed where to chose the "FastAPI" application. A json file will be displayed, insert the following body, if required adapt it
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
To include unit tests pytest is used, more informations on its usage are availabele [here](https://docs.pytest.org/en/7.3.x/)
Two scripts for testing are included in this project with `Pipfile`:
1. List only the tests
```shell
$ pipenv run tests-list
```

2. Run the tests
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