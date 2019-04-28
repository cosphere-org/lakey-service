
SHELL := /bin/bash


help:  ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


.PHONY: install
install:  ## install all dependencies
	python -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt
