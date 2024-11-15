#!/bin/bash

# Delete Deplyments and services
# kubectl delete all --all
# kubectl delete pvc postgres-pvc
# kubectl delete ingress --all

# Create deployments and services
cd kubernetes
kubectl apply -f database-service-deployment.yaml
kubectl apply -f product-service-deployment.yaml
kubectl apply -f user-auth-service-deployment.yaml
kubectl apply -f home-service-deployment.yaml
kubectl apply -f customer-service-deployment.yaml
kubectl apply -f order-service-deployment.yaml