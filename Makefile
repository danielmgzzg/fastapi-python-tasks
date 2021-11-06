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
