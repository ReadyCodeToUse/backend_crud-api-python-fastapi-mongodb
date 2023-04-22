# Secured containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.

## Before you start
Make sure docker is installed, if you need to install it reefer to the [official documentation](https://docs.docker.com/engine/install/), if you are using Windows i suggest the use of WSL and installation via WSL engine.

==!!!IMPORTANT!!!==
Move inside the directory where this README is located to execute all of the commands in this README.md
```shell
$ cd %path-to-the-repository%/fastapi
```

##  Required steps
Type in your shell:
```shell
$ cp .env.example .env
``` 
The contained variables are for the database administrator, required for an API to make updates.

## Start the instance
A docker compose file is provided in this directory to try and launch locally the db instance alone, to do so execute then the folloing command:
```shell
$ docker-compose up --build -d
```

To run in detatched mode the ```-d``` flag has been added.

When starting the mongodb instance will be initialized with the `docker-entrypoint-initdb.d/mongo-init.js` script. If any modification in the configuration, collection creation is required just update this scripts to fit your needs.

A file `users.json` can be used to store some data to upload some data and not hardcode the informations inside the initialization script.
## Stop the instance
When you are done working and stop the instances there are two options:
1. Stop the instance but keep the container up 
```shell
$ docker-compose stop
```

2. Stop the instance and delete the contaier
```shell
$ docker-compose down
```

**IMPORTANT** Both commands must be ran from this directory which contains the `docker-compose.yml` file.

**IMPORTANT** By default the provided `docker-compose.yml` uses anonymus volumes to store the DB data, if you want to store it in a specific directory just uncomment `docker-compose.yml line 9`.

**IMPORTANT** By default the provided `docker-compose.yml` uses anonymus volumes to store data, running the second command will not delete automatically the data (default docker behaviour). To free some some space up if the data is not required and can be deleted type from your command line
```shell
docker volumes prune
```
to delete all zombie volumes.