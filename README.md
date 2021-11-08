# FastAPI Uvicorn Tasks API

[Link to demo](https://tasks-api-python.azurewebsites.net/docs/)

API using FastAPI, Pydantic models, and MongoDB

OpenAPI documentation models for requests, responses and errors.

## Requirements

- Python >= 3.7
- Docker
- Requirements listed on [requirements.txt](requirements.txt)
- MongoDB connection string
- Make (You can use a Mac, Linux or WSL in Windows) for build and deploy

## **Running development server**

this will run nodemon with hot reloading, don't worry the mounted volumes with compose are only in development!

`make start`

Visit [http://localhost:5000/](http://localhost:5000/)

## **Running production server**

`make prod`

It's important to set the following variables in order to connect to the production server. Why not a connection string? I find it easier to integrate the different parameters with greater control. It will be necessary to configure and deploy a CosmosDB instance with MongoDB API for instance.

```
// .env

API_PORT=
MONGO_URI=
MONGO_DB=

// if you are running the local instance of the client you will need this to add it to cors programatically, depending on the port
CLIENT_URI=http://localhost   or   CLIENT_URI=http://localhost:3000

```

Visit http://localhost:${API_PORT}

## **Building & Running production image**

This will build and tag the production image locally for testing. If everything is working as it should then it can be published to Azure Container Registry

`make build`

This will run the production image locally and inject the necessary environment variables from .env to ensure its funcionality

`make run`

## **Deploying to Azure**

### **Prerequisites:**

- Create a free Azure account at [https://azure.microsoft.com/free](https://azure.microsoft.com/free)
- Have Azure CLI installed in Linux environment either Mac or PC with WSL 2
- Login with Azure CLI
- Docker

Configure this app environment variables with your project-specific details for Make file:

```
// .env

REGISTRY_NAME=
RESOURCE_GROUP=
REGISTRY_IMAGE=
REGISTRY_TAG=
APP_SERVICE_PLAN=
APP_NAME=
```

If your infrastructure is already setup and you have this variables then, you can continue with the following steps

### **Build and publish the container to Azure Container Registry:**

`make acr-build`

Since Azure Container Registry builds sometimes pop up some errors, it's also possible to build with Docker locally and publish to your registry using

`make build`

`make publish`

## Infrastructure

> If you want to provision the whole infrastructure from here, it is possible using the Makefile, and the following environment variables are connected, which run all the necessary scripts, otherwise, you can set the environment variables from existing resources.

### 1) Create an App Service plan

`make appservice-create`

### 2) Create Web App from Container image

`make webapp-create`

### 3) Update Web App environment variables as expected by the app code (it takes them from .env)

`make webapp-appsettings`

### 4) Granting the web app with a system-managed identity

`make app-permissions`

### 5) Grant the container identity permission to access the registry

`make container-permission`

### 6) Configure app to use the managed identity to pull from Azure Container Registry.

`make resource-identity`

### 7) **Build and publish the container to Azure Container Registry:**

`make acr-build` or `make build` & `make publish`

### 8) Use the deploy command to specify the container registry and the image for the web app

`make deploy`

### 9) Retrieve the web app's container settings and verify all is in order

`make container-settings`

## **Stack**

- FastAPI
- Uvicorn
- Gunicorn (For production)
- PyMongo

## **Opportunities**

- Logging Middleware
- Testing
- Caching
