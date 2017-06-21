# fermiq_docker
Docker Setup for FermiLib+ProjectQ

This Docker image will allow users to easily install FermiLib and ProjectQ (version with the fast simulator). Check out Docker's [website](https://www.docker.com/what-container) that describes what a container image is and why it can be so useful. 

## What is included?
- Conda Python 3 (but you can also use Python 2 with one minor change in Dockerfile. See Dockerfile for instructions.)
- [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ) (+ its dependencies)
- [FermiLib](https://github.com/ProjectQ-Framework/FermiLib.git) (+ its dependencies)

## Usage

To use this image, you first need to install [Docker](https://www.docker.com/).

After installing Docker, move this Dockerfile to your working directory.

You now have two options: pulling the Docker image from Docker Hub or building the image.

To pull the Docker image, execute:

```
docker pull hsim13372/fermiq_docker
```
 
To build the Docker image, execute:

```
docker build .
```

Finally, to run the image (assuming you're still inside your working directory), execute:

```
docker run -d -it -v "$(pwd)" hsim13372/fermiq_docker
```

