# Secured containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.

**Before doing anything make sure docker is installed!**

# Required steps
Type in your shell:
```sh
$ cp .env.example .env
``` 
and then update the environement variables in it.

You are porovided an example dotenv file in ```${root}/env``` directory containing some key values for the mongodb docker image to start correctly.

The following variables are the variables to initialize the mongo container as you can see [here](https://hub.docker.com/_/mongo/)
- MONGO_INITDB_ROOT_USERNAME
- MONGO_INITDB_ROOT_PASSWORD
- MONGO_INITDB_DATABASE

The variables are for the database administrator, which is required for an API to make updates.

A docker compose file is provided in this directory to try and launch locally the db instance alone, to do so execute then the folloing command:
```sh
docker-compose --env-file ../env/example.db.env up --build -d
```


To run in detatched mode the ```-d``` flag has been added.