#!/bin/bash

kubectl delete deployments customer-service fashionme-db home-service order-service product-service user-auth-service

# Build docker images for each microservices and push them into the docker hub
cd product-service
docker build -t jayanisathukorala/product-service:latest .
docker push jayanisathukorala/product-service:latest

cd ../user-auth-service
docker build -t jayanisathukorala/user-auth-service:latest .
docker push jayanisathukorala/user-auth-service:latest

cd ../database-service
docker build -t jayanisathukorala/fashionme-db:latest .
docker push jayanisathukorala/fashionme-db:latest

cd ../home-service
docker build -t jayanisathukorala/home-service:latest .
docker push jayanisathukorala/home-service:latest

cd ../customer-service
docker build -t jayanisathukorala/customer-service:latest .
docker push jayanisathukorala/customer-service:latest

cd ../order-service
docker build -t jayanisathukorala/order-service:latest .
docker push jayanisathukorala/order-service:latest

# Create deployments and services
cd ../kubernetes
kubectl apply -f database-service-deployment.yaml
kubectl apply -f product-service-deployment.yaml
kubectl apply -f user-auth-service-deployment.yaml
kubectl apply -f home-service-deployment.yaml
kubectl apply -f customer-service-deployment.yaml
kubectl apply -f order-service-deployment.yaml

