# Makefile

include .lily/lily_assistant.makefile
include .lily/lily.makefile


.PHONY: create_db
create_db:  ## create dockerized postgres db server
	source env.sh && \
    docker run -d --name lakey-service-db \
      --env-file <(env | grep POSTGRES) \
      -p 5433:5432 \
      postgres

.PHONY: start_db
start_db:   ## start dockerized postgres db server
	docker start lakey-service-db

.PHONY: stop_db
stop_db:   ## stop dockerized postgres db server
	docker stop lakey-service-db
