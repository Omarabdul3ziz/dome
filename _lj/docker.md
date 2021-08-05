# Syntax
`docker-compose build`
`docker-compose up` `-d`: deattached -running in the background
`docker-compose down`

`sudo docker pa -a` list the running containers.
`sudo docker images` list images
`sudo docker rm <container-id>`
`sudo docker id <image-id>`

`sudo docker tag <image-name>:<image-tage> <hub-username>/<hub-repo-name>` rename
`sudo docker push <hub-username>/<hub-repo-name>` push

# Errors
`If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.`
try using `sudo docker-compose up`