### Usage

```
docker network create --driver bridge net
docker volume create vol

docker container run -d -v vol:/opt/vlang/app/ -p 90:5000 --name vlang --network=net omarabdul3ziz/vlang_api
docker container run -d -p 91:8080 --name vue --network=net omarabdul3ziz/vue_ui
```

Go to http://localhost:91/
