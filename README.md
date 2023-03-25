# Composer template
This is a simple template for a docker compose application with a DB managed by a FastAPI API.
All of this exists to provide a template of boilerplate code created to help me in the future to do similar things and made available so you can use it as well.

**Before doing anything make sure docker is installed!**

# Required steps
Here you can find informations and steps to start the project.

## Create the environment variables
To start this application some environement variables are required.
Simply follow the next steps to generate the two required files.

## DB
Some operations may be required to fully understand this section, when completed make sure to read the following documentation [here](./mongo/README.md).

For this step you can copy in the ```./env``` directory the ```./env/example.env``` as ```.db.env```, if you prefer type in your shell
```sh
$ cp ./env/example.db.env ./env/.db.env
```
the file can be copied without any changes.

## API
Some operations may be required to fully understand this section, when completed make sure to read the following documentation [here](./fastapi/README.md).

For this step the ```./fastapi/scripts/init.sh``` script will be used.

You can type ```$ ./fastapi/scripts/init.sh $(pwd)/env/.api.env``` to generate the file and provide the required inputs:
- db username -> admin
- db password -> admin
- db host -> db (which is the db containers name)
- db port -> 27017
- db name -> fastapi-auth-template

The produced file will be something similar to this:
```dotenv
SECRET_KEY=super-secret-key-automatically-generated
CONFIGS_DIR=/app/configs
LOGGING_DIR=/app/logs
DB_USERNAME=admin
DB_PASSWORD=admin
DB_HOST=db
DB_PORT=27017
DB_NAME=fastapi-auth-template
```

As you can see there are two directories: configs and logging.
This have been set by default to ```/app/something-else``` because in the composer file the container volumes will be mounted in those directories.

An example file named ```example.api.env``` can be found in 


## Start the containers
Now that the environment variables are created you can launch the containers with 
```sh
$ docker-compose up --build
``` 
so the fastapi-auth-template image will be build and then the required containers will be generated.

To test everything's working just fine you can firs check the connection to the connecting to mongodb by typing the following connection string inside MongoDB compass ```mongodb://admin:admin@localhost:27017/fastapi-auth-template``` (here we are using the localhost becuase we provided ports in docker compose to map the mongodb instance container with our localhost). After you were able to connect check the api is working correctly by typeing 
```sh
$ curl http://localhost:8000/cdrt/
```
in your shell and it should return an "Hello, world" like message. Alternatively to explore the available api you can type in your browser http://localhost:8000/docs, and it should return the swagger documentation

### Notes
Currenlty no networks in the docker-compose file are used, and to let the api container connect to the containerized db the api must have ```db``` as host, because is the db container name and it work as an host from container to container.
