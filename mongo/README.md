# Secured containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.

**Before doing anything make sure docker is installed!**

# Required steps
You are porovided an example dotenv file in ```${root}/env``` directory containing some key values for the mongodb docker image to start correctly.

To see the environment variables to initialzie look [here](https://hub.docker.com/_/mongo/), following the example structure of the dotenv file:
```sh
    MONGO_INITDB_ROOT_USERNAME=root
    MONGO_INITDB_ROOT_PASSWORD=root
    MONGO_INITDB_DATABASE=fastapi-auth-template
    DB_ADMIN_USERNAME=admin
    DB_ADMIN_PASSWORD=admin
```

The variables are for the database administrator, which is required for an API to make updates.

A docker compose file is provided in this directory to try and launch locally the db instance alone, to do so execute then the folloing command from inside this directory:
```sh
docker-compose --env-file ../env/example.db.env up --build -d
```


To run in detatched mode the ```-d``` flag has been added.