# Run Instructions

## Run Stundenplan via Docker Compose (Linux and Windows)

Make sure docker and docker compose are installed.

Start the Docker engine (e.g. start Docker Desktop).

Start a terminal window in the project root folder.

Run `docker compose up` to see the list of arguments which can be used.

In Linux terminal use `COMMAND="[ARGS]" docker compose up` to run the algorithm in a docker container. 

In Windows powershell use `$env:COMMAND="[ARGS]"; docker compose up` to run the algorithm in a docker container. 

## Run Stundenplan via a Docker Script (Windows)

Start the Docker engine (e.g. start Docker Desktop).

Start a terminal window (Powershell) in the project root folder.

Run the script: 
`.\Docker_Launcher.ps1 [ARGS]`

## Run Stundenplan manually via Docker (Linux and Windows)

Start the Docker engine (e.g. start Docker Desktop).

Start a terminal window (Powershell) in the project root folder.

Use the Dockerfile to build an image:
`docker build --tag stundenplan_image .`

[**Optional**] Remove dangling images:
`docker image prune --force`

Use the image to build and run a container:
`docker run --rm --name stundenplan_container --volume ${PWD}/output:/app/output stundenplan_image [ARGS]`

# Developer Instructions

## Dependency management

Start a terminal window (Powershell) in the project root folder.

To download the required packages/dependencies, run:
`pip3 install -r requirements.txt .`

To add additionally installed packages/dependencies to the requirements file, run:
`pip3 freeze > requirements.txt`

