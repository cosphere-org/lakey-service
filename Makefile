# Makefile

include .lily/lily_assistant.makefile
include .lily/lily.makefile


start_ngrok:  ## start ngrok proxy server
	source env.sh && \
	ngrok start --config ngrok_private.yml --region eu --all
