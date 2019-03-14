# Makefile

SHELL := /bin/bash

help:  ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:  ## install all dependencies and create virtualenv
	source env.sh && \
	python -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt && \
	pip install -r test-requirements.txt

#
# DEVELOPMENT
#
shell:  ## run django shell (ipython)
	source env.sh && python lakey_service/manage.py shell

runserver:  ## run development server (for quick checks)
	source env.sh && python lakey_service/manage.py runserver

#
# TESTS
#
test:  ## run selected tests
	source env.sh && py.test -r w -s -vv $(tests)

test_all:  ## run all available tests
	source env.sh && py.test -r w -s -vv tests

#
# UPGRADE_VERSION
#
upgrade_version_patch:  ## upgrade version by patch 0.0.X
	source env.sh && python lakey_service/manage.py upgrade_version PATCH

upgrade_version_minor:  ## upgrade version by minor 0.X.0
	source env.sh && python lakey_service/manage.py upgrade_version MINOR

upgrade_version_major:  ## upgrade version by major X.0.0
	source env.sh && python lakey_service/manage.py upgrade_version MAJOR

#
# START
#
start:  ## start service locally
	source env.sh && \
	python lakey_service/manage.py migrate && \
	cd lakey_service && \
	gunicorn conf.wsgi \
		--worker-class gevent \
		-w 1 \
		--log-level=debug \
		-t 60 \
		-b 127.0.0.1:8000

migrate:  ## migrate
	python lakey_service/manage.py migrate
