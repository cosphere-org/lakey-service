# Makefile

include .lily/lily_assistant.makefile
include .lily/lily.makefile


#
# DATABASE
#
.PHONY: create_db
create_db:  ## create dockerized postgres db server
	source env.sh && \
	docker run -d --name lakey-service-db \
		--env-file <(env | grep POSTGRES) \
		-p 5433:5432 \
		postgres


.PHONY: start_db
start_db:  ## start dockerized postgres db server
	docker start lakey-service-db


.PHONY: stop_db
stop_db:   ## stop dockerized postgres db server
	docker stop lakey-service-db


#
# FAKERS
#
.PHONY: create_fake_catalogue_items
create_fake_catalogue_items:  ## create fake catalogue items
	source env.sh && \
	python lakey_service/manage.py create_fake_catalogue_items


.PHONY: create_fake_catalogue_items_with_overwrite
create_fake_catalogue_items_with_overwrite:  ## create fake catalogue items with overwriting existing
	source env.sh && \
	python lakey_service/manage.py create_fake_catalogue_items --overwrite


#
# ADMIN
#
start_gunicorn_admin:  ## start service locally
	source env.sh && \
	export PYTHONPATH="${PYTHONPATH}:${PWD}/lakey_service" && \
	gunicorn conf.wsgi_admin \
		--worker-class gevent \
		-w 1 \
		--log-level=debug \
		-t 60 \
		-b 127.0.0.1:10000
