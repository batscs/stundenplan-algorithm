# Use the Dockerfile to build an image:
docker build --tag stundenplan_image $PSScriptRoot
# [Optional] Remove dangling images:
docker image prune --force
# Use the image to build and run a container:
docker run --rm --name stundenplan_container --volume $PSScriptRoot/output:/app/output stundenplan_image $args