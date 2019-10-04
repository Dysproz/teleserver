.DEFAULT_GOAL := help

help: ## Show help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install: ## install teleserver
	./install.sh

uninstall: ## uninstall teleserver
	./uninstall.sh

test: ## test teleserver
	tox

