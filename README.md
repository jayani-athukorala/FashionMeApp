# Fashion Me E-commerce Application

Welcome to the Fashion Me e-commerce application repository!

## Description

"Fashion Me" is a microservices-based e-commerce application designed for managing an online fashion store. The application enables user authentication, customer management, product management, and order management, all encapsulated within their own microservices for scalability, modularity, and ease of maintenance.

## Software Architecture Overview

The Fashion Me application is built upon a microservices architecture, where each service is responsible for a specific functionality:

- **User-Auth Service:** Handles admin login and session-based authentication.
- **Product Service:** Manages product listing, addition, removal, and updates.
- **Customer Service:** Deals with customer listing and addition.
- **Order Service:** Handles order listing and status updates.
- **Database Service:** Provides a centralized database service for data storage and retrieval, using PostgreSQL with Docker and Kubernetes Persistent Volumes.

## Implementation Steps

1. **Dockerize the Microservices:** Create Dockerfiles for each microservice and build Docker images.
2. **Build and Push Docker Images:** Use Docker commands to build and push Docker images to Docker Hub.
3. **Create Kubernetes Deployment Files:** Define Kubernetes deployment files for each microservice.
4. **Deploy the Database Microservice:** Configure a Kubernetes deployment file for the Database Service and persistent volume.
5. **Apply Kubernetes Deployment:** Deploy the Fashion Me application onto Minikube using Kubernetes manifests.
6. **Expose Microservices:** Apply Ingress resources to expose services to the outside world.
7. **Access the Application:** Access the application using the defined hostname (fashionme.com).

## Benefits and Challenges

### Benefits

- **Scalability:** Independent scaling of services allows efficient handling of varying loads.
- **Flexibility:** New features can be added or modified without impacting other parts of the application.
- **Resilience:** Microservices architecture combined with Kubernetes enhances overall reliability.
- **Modularity:** Independent development and deployment of each service promote easier maintenance.

### Challenges

- **Complexity:** Managing multiple services and their interactions can be complex.
- **Data Consistency:** Ensuring data consistency across services using different databases can be challenging.
- **Monitoring and Logging:** Comprehensive monitoring and logging are required for optimal performance and debugging.
- **Communication:** Effective communication mechanisms between microservices can increase complexity.

## Repository Structure

The repository structure is organized as follows:

- `user-auth-service/`: Source code and Dockerfile for the User-Auth microservice.
- `product-service/`: Source code and Dockerfile for the Product microservice.
- `customer-service/`: Source code and Dockerfile for the Customer microservice.
- `order-service/`: Source code and Dockerfile for the Order microservice.
- `database-service/`: Source code, Dockerfile, and Kubernetes deployment files for the Database microservice.
- `kubernetes/`: Kubernetes deployment files for deploying the application onto Minikube.
- `README.md`: This README file providing an overview of the project.

## Getting Started

To get started with the Fashion Me application, follow these steps:

1. Clone this repository to your local machine.
2. Set up Docker and Minikube environment.
  Docker
  Minikube
    Minikube addons: minikube addons enable ingress, minikube addons enable ingress-dns
  Kubernetes
    kubectl
4. Build Docker images for each microservice.
5. Deploy the application onto Minikube using Kubernetes deployment files. (docker_build.sh can be used)
5. Access the application using the defined hostname (fashionme.com).
