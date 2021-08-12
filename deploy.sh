#!/bin/bash

echo "Creating the volume..."
kubectl apply -f ./k8s-conf/volume.yaml

echo "Creating the database credentials..."
kubectl apply -f ./k8s-conf/secret.yaml

echo "Deploying mongodb..."
kubectl apply -f ./k8s-conf/mongo.yaml

echo "Deploying flask api..."
kubectl apply -f ./k8s-conf/flask.yaml

echo "Adding the ingress..."
minikube addons enable ingress
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
kubectl apply -f ./k8s-conf/ingress.yaml

echo "Adding to hosts..."
echo "$(minikube ip) do.me" | sudo tee -a /etc/hosts

echo "Deploying Vue ui..."
kubectl create -f ./k8s-conf/vue.yaml