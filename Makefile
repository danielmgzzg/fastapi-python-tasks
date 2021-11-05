start:
	docker-compose up

down:
	docker-compose down

rm-all:
	make rmi && make rmv
	
rmi:
	@echo "\n[ Removing Containers, networks & images ]"
	docker-compose down --rmi all

rmv:
	@echo "\n[ Removing all attached volumes ]"
	docker-compose down -v
