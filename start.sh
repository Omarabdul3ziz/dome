#!/bin/bash

sudo systemctl start mongod
echo "DB server started on localhost in port 27017"

go run ./services/server/main.go &
echo "API server started on localhost in port 5000."

cd ./services/client
npm run serve &
echo "UI server started on localhost in port 8080"