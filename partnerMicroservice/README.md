to build the docker container:
docker build -t partner-microservice .
to run the docker container:
docker run -p 65435:65435 partner-microservice

Need to:
- figure out logging and where all of the print statements go
- figure out how to get the docker container to run on the server
- figure out how to have the docker container store the database on the server and not in the container
- run the docker container to run on the server on startup
