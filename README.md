# fermiq_docker
Docker Setup for FermiLib+ProjectQ

This Docker image will allow users to easily install FermiLib and ProjectQ (version with the fast simulator). Check out Docker's [website](https://www.docker.com/what-container) that describes what a container image is and why it can be so useful. 

## What is included?
- Conda Python 3 (but you can also use Python 2 with one minor change in Dockerfile. See Dockerfile for instructions.)
- [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ) 
- [FermiLib](https://github.com/ProjectQ-Framework/FermiLib.git)

## Usage

To use this image, you first need to install [Docker](https://www.docker.com/).

After installing Docker, there are two options: (1) pulling the Docker image from Docker Hub or (2) building the image.

(1) To pull the Docker image, execute:

```
docker pull hsim13372/fermiq_docker
```
 
(2) To build the Docker image, move the [Dockerfile](https://github.com/hsim13372/fermiq_docker/blob/master/Dockerfile) to your working directory. Then execute:

```
docker build -t "hsim13372/fermiq_docker" .
```

Finally, to run the image (assuming you're still inside your working directory), execute:

```
docker run -d -it -v "$(pwd)" hsim13372/fermiq_docker
```

