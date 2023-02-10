# Svelte, Falcon, mySQL Project Template

This is a template for my projects using Svelte, Falcon, mySQL. This Template utlizes Docker and Docker Compose to host the servers. 

This template includes a simple frontend using the JavaScript framework Svelte that connects to a backend API written in python using the Falcon library. The application also consists of a MySQL database and a phpMyAdmin server to allow developers to visualize their data. An Nginx reverse proxy is set up to allow access to the frontend and the API layers. All the servers are run in docker, with docker-compose bringing up all the servers. 

This project also includes code for performing unit tests in python using the Pytest library. Lastly, the project contains tools for creating python documentation using Sphinx. 

Each folder has a ReadMe.md file that goes into more depth on using the tools available and how to use those tools to develop your applications. 

## Technologies Used
Frontend - [Svelte](https://svelte.dev/)
CSS - [TailwindsCSS](https://tailwindcss.com/)
Backend - [Faclon](https://falconframework.org/)
Database - [mySQL](https://www.mysql.com/)
Database Visualization - [phpMyAdmin](https://www.phpmyadmin.net/)
Reverse Proxy -[Nginx](https://www.nginx.com/)
Running the Application -  [Docker](https://www.docker.com/)
Testing - [Pytest](https://docs.pytest.org/en/7.2.x/)
Documentation - [Shpinx](https://www.sphinx-doc.org/en/master/)

## Prerequisites
1. [Docker](https://docs.docker.com/engine/install/)
	1. I recommend installing [Docker Desktop](https://www.docker.com/products/docker-desktop/)
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

### Accessing the Frontend
1. In your browser go to http://localhost:80
1. If the fronend server is running you will see a default page.
1. Then navigate to http://localhost:80/tests to verify the frontend is connected to the backend
2. If the backend is running you will see {alive: true}

### Accessing the Backend
1. In your browser go to http://localhost:80/api/v1/
1. If the API server is running you will get a responce {alive: true}

## Development

Each folder contains in-depth information on how to begin development. I recommend using [VS Code](https://code.visualstudio.com/) as your editor. I found the following VS Code Extensions helpful:
- [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Svelte for VS Code](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode)
- [Tailsind CSS Intellisence](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)