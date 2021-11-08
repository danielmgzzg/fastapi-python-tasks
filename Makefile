include .env
start:
	docker-compose up --build

down:
	docker-compose down

prod:
	@echo "\n[ Spinning up Docker Compose production environment ]"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build

rm-all:
	make rmi && make rmv
	
rmi:
	@echo "\n[ Removing Containers, networks & images ]"
	docker-compose down --rmi all

rmv:
	@echo "\n[ Removing all attached volumes ]"
	docker-compose down -v

run:
	@echo "\n[ Running prod image ]"
	docker run -p 8000:8000 --env-file ./.env ${REGISTRY_NAME}.azurecr.io/tasks-api-py:prod

az-group-create:
	@echo "\n[ Creating Azure Resource Group ]"
	az group create --name ${RESOURCE_GROUP} --location westeurope

acr-create:
	@echo "\n[ Creating Azure Container Registry ]"
	az acr create --name ${REGISTRY_NAME} --resource-group ${RESOURCE_GROUP} --sku standard --admin-enabled true

acr-build:
	@echo "\n[ Using Azure Container Registry to build images... ]"
	az acr build --file ./api/Dockerfile --target prod --registry ${REGISTRY_NAME} --image ${REGISTRY_IMAGE}:${REGISTRY_TAG} ./api

build:
	@echo "\n[ Build API production image ]"
	docker build ./api --target prod \
	--tag ${REGISTRY_NAME}.azurecr.io/${REGISTRY_IMAGE}:${REGISTRY_TAG}

login:
	@echo "\n[ log into private registry ]"
	az acr login --name ${REGISTRY_NAME}

publish: login
	@echo "\n[ publish production grade images ]"
	docker push ${REGISTRY_NAME}.azurecr.io/${REGISTRY_IMAGE}:${REGISTRY_TAG}
	@echo "\n[ Verifying if push was successfull ACR repo list... ]"
	az acr repository list -n ${REGISTRY_NAME}

appservice-create:
	@echo "\n[ Creating an App Service plan ]"
	az appservice plan create --name ${APP_SERVICE_PLAN} \
	--resource-group ${RESOURCE_GROUP} --is-linux

webapp-create:
	@echo "\n[ Creating Web App from Container image ]"
	az webapp create --resource-group ${RESOURCE_GROUP} \
	--plan ${RESOURCE_GROUP} --name ${APP_NAME} \
	--deployment-container-image-name ${REGISTRY_NAME}.azurecr.io/${REGISTRY_IMAGE}:${REGISTRY_TAG}

webapp-appsettings:
	@echo "\n[ Updating Web App environment variables as expected by the app code ]"
	az webapp config appsettings set --resource-group ${RESOURCE_GROUP} \
	 --name ${APP_NAME} --settings API_PORT=${API_PORT} WEBSITES_PORT=${API_PORT} \
	 MONGO_DB=${MONGO_DB}  MONGO_URI=${MONGO_URI}  CLIENT_URI=${CLIENT_URI}\
	 

app-permissions:
	@echo "\n[ Granting the web app with a system-managed identity ]"
	az webapp identity assign --resource-group  ${RESOURCE_GROUP} --name ${APP_NAME} --query principalId --output tsv

container-permission:
	@echo "\n[ Granting the container identity permission to access the registry ]"
	az role assignment create --assignee $(shell az webapp identity assign --resource-group  ${RESOURCE_GROUP} --name ${APP_NAME} --query principalId --output tsv) \
	 --scope /subscriptions/$(shell az account show --query id --output tsv)/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.ContainerRegistry/registries/${REGISTRY_NAME} \
	 --role "AcrPull"

resource-identity:
	@echo "\n[ Configuring app to use the managed identity to pull from Azure Container Registry. ]"
	az resource update --ids /subscriptions/$(shell az account show --query id --output tsv)/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Web/sites/${APP_NAME}/config/web \
	--set properties.acrUseManagedIdentityCreds=True

deploy:
	@echo "\n[ Using the deploy command to specify the container registry and the image for the web app ]"
	az webapp config container set --name ${APP_NAME} --resource-group ${RESOURCE_GROUP} \
	--docker-custom-image-name ${REGISTRY_NAME}.azurecr.io/${REGISTRY_IMAGE}:${REGISTRY_TAG} \
	--docker-registry-server-url https://${REGISTRY_NAME}.azurecr.io

container-settings:
	@echo "\n[ Retrieving the web app's container settings ]"
	az webapp config container show --name ${APP_NAME} --resource-group ${RESOURCE_GROUP}