# Project Template

This is a template for my projects using Svelte, Falcon, and Nginx. This Template utlizes Docker and Docker Compose to host the servers. 

## Prerequisites
1. [Docker](https://docs.docker.com/engine/install/)
2. [Docker Compose](https://docs.docker.com/compose/install/)
3. [Git](https://git-scm.com/)
4. [Python](https://www.python.org/downloads/release/python-3108/) 3.11.1 suggested 


## Setup
1. Ensure that Docker is running
	- If you are using Docker Desktop you can open the appliction to start the Docker Service
1. From your command line run `git clone https://github.com/CollinConnors/ProjectTemplate.git`
2. `cd ProjectTemplate`
3. `docker compose -f "dockercompose.yaml" up -d --build`
	- If you are using the VSCode Docker Extension you can right click the dockercompose.yaml and select "Docker Compose Up"

## Accessing the Frontend
1. In your browser go to http://localhost:80 
1. If the all the servers are running correctly you will see a page letting you know everything is working
1. Then navigate to http://localhost:80/tests to verify the frontend is connected to the backend 

## Testing
1. After setting up the project run `cd tests`
2. `pip install -r requirements.txt`
3. `pytest backend_tests.py`
4. If the network was built succesfully you should pass all tests

## Building Docs
1. After setting up the project run `cd docs`
2. `pip install -r requirements.txt`
3. Run the make file 
	- On Windows it is `.\make.bat html`
	- On Mac/Linux it is `make html`
4. Inside _build/html ther is an index.html that will bring you to the docs page
