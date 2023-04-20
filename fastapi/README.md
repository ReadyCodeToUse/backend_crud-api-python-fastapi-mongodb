# FastAPI API tempalte
This is an example of how to dockerize a python FastAPI REST API with auth.

This is an example python project to demonstate the following points:
- python project structure example suitable for most projects
- pytest and TDD (Test Driven Development)
- containerization
- use of python best practices (PEP8) (To be added)
- pylint (To be added)
- use of pre-commits (To be added)

This demo contains a REST API built over FastAPI, this repository can be used as a starting point for other projects too and not only REST API. 

## Before you start
Make sure docker, pyenv and pipenv are installed, if you need any of this tools reefer to the following sources:
- [pyenv](https://github.com/pypa/pipenv)
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

### Prepare the environment
To prepare the development environment some steps are required, some commands inside the cli are required:
* search the latest 3.10 available python version
```shell
    pyenv install --list | grep "3.10."
```

* install the latest python version python 3.10 
```shell
    pyenv isntall 3.10.x # replace the x with the latest fix number available
```

TO CONTINUE


# General informations
In this sections the general informations about the project are presented.
To execute local developement simply follow the ahead steps, if you prefer develop within a container or docker compose(at the moment is not available) follow [this section](#docker)

## Initialization
To run the application some environement variables are required, it is possible to generate them via the ```init.sh``` script. You can simply type from the root of the repository
```sh
    $ chmod 777 ./scripts/init.sh && ./scripts/init.sh
```
to launch the script. Arguments are required to run the script, the last one will be a ".env" file an absolute file path is required, it is not mandatory that it's an existing file because it will be generated if required.\
The following naming convention has been decided:
- ```.dev.env``` for the developement environement.
- ```.test.env``` for the test environement (the only difference now are the variables for the DB connection like port, host and so on).


## Start-up
The application is not containerized right now (it soon will), and to startup the developement environement 2 options are available:
- Run from terminal
- Run from IDE

To run the application via terminal the ```serve_dev.sh``` script is available, simply execute it with ```$ chmod 777 ./scripts/serve_dev.sh && ./scripts/serve_dev.sh absolute/path/to/.dev.env```

Otherwise if you're using VsCode (I know it's not an IDE but a text editor really close to a IDE if customized), in the debug configuration you can add a new configuration for python programs, then a new menu is displayed where to chose the "FastAPI" application. A json file will be displayed, insert the following body, if required adapt it
```json
{ 
    "name": "Python: FastAPI DEV",
    "type": "python",
    "request": "launch",
    "module": "uvicorn",
    "args": [
        "src.app:fastapi_app",
        "--reload"
    ],
    "jinja": true,
    "justMyCode": false,
    "envFile": "${workspaceFolder}/env/.dev.env"
}
```

by doing so yow will be able to run and insert debug points into the application and debug it visually.

*TO RUN THE API WITH VSCODE IN THIS WAY YOU HAVE TO FOLLOW THE STEPS OF THE [Testing](#testing) section to build the module locally.*

## Testing
To run the available unit tests inside ```$(pwd)/tests/``` run from your shell:
```$ chmod 777 ./scripts/test.sh && ./scripts/test.sh $(pwd)```.
This will install locally the ```src``` module inside the ```api``` directory.

which will make the script executable and then perform the action described at [this section](#scripts).

To then execute the tests you can either run them from you IDE (VsCode in my case) or terminal with ```pytest --envfile=$(pwd)/env/.test.env``` this flag exists because of the ```pytest-dotenv``` plugin for pytest present in the requirements.txt file.

# Docker
A developement container is available in ```Docker``` folder. First build the image as follow from the repository root folder ```$ docker build -f ./Docker/Dockerfile.dev . -t fastapi_auth_template_api:0.0.0-dev```. After that you can run it by typing ```$ docker run --name fastapi_auth_template_api-0.0.0-dev -v $(pwd)/api/src:/app/src -v $(pwd)/configs:/app/configs -p 8000:8000 --env-file ./env/.container.dev.env --add-host=host.docker.internal:host-gateway -id fastapi_auth_template_api:0.0.0-dev```.

Before doing that two things are required:
- Having installed a MongoDB server instance (I installed mine usign a mongo docker image)
- Generate a new .env file, and following the convention I decided when starting this repository the name I choosed is ```.container.dev.env```.

To generate the .env file simply type in the shell ```$ ./scripts/init.sh container .container.dev.env``` this will tell the script that you want to generate a new .env file for a container, and by doing so the configs and log directory are setted by default, other than that the suggested db host will be ```host.docker.internal``` if you are using a db server installed on your machine (like a docker image of MongoDB).

This container can be launched alone by it self, but we suggest to run it with docker compose when testing a complete application e.g. FE+BE+DB(coming soon).

VSCode provide an extension ```Remote - Containers``` which will help build development containers, simply open the command palette and search for ```Open folder in container``` if is your first time creating one, otherwise if you already have a container search for ```Attach to running container```. This will generate a container container where you will be able to follo the [local development](#local-development) steps to configure the environment. A good thing of this extension is that the github repository is mounted as a volume, so the code will be modified directly on your machine and you will not need to do strange steps to sync the code in the container and your machine.

# Notes
I presonally use pyenv combined with pyenv-virtualenv when developing in a local environement, outside of a container (if this can help someone), but now my workflow will be replaced with the container development thantks to Visual Studio Code, if you are using a different IDE/Text Editor and you want to contribute adding documentation for it don't hesitate to contact me and send me you workflow to integrate in here :smile:.