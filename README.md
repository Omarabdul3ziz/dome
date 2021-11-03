### Usage

1. Create network and volume

```
docker network create net
docker volume create vol
```

2. Start API server

```
docker container run \
-d \
-v vol:/opt/vlang/app/ \
-p 90:5000 \
--net net \
--name api \
omarabdul3ziz/vlang_api
```

3. Start UI client

```
docker container run \
-d \
-e VUE_APP_API_URL=http://172.0.0.3:90 \
-p 91:8080 \
--net net \
--name ui \
omarabdul3ziz/vue_ui
```

4. Go to http://localhost:91/
