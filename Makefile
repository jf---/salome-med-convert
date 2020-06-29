SALOMEMECA_MEDCONVERTER_ROOT_DIR ?= ./install
PREFIX = ${SALOMEMECA_MEDCONVERTER_ROOT_DIR}
TRAD_DIR = resources/medconverter

SPHINXHTMLDIR = ${SALOMEMECA_MEDCONVERTER_ROOT_DIR}/share/doc/salome/gui/medconverter/html
SPHINXROOTDIR = doc/sphinx

.PHONY: help install uninstall clean doc

help: ## Print Help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

translate: ## Build the i18n files (extract messages and compile 'qm' file)
	pylupdate5 $(TRAD_DIR)/medconverter.pro
	lrelease $(TRAD_DIR)/medconverter.pro

doc :
	sphinx-build -b html $(SPHINXROOTDIR) $(SPHINXHTMLDIR)

install: ## Install the plugin into directory given by $SALOMEMECA_MEDCONVERTER_ROOT_DIR
	make translate
	python setup.py install --prefix=$(PREFIX)
	python setup.py clean --all
	make doc

uninstall: ## Uninstall a previous installation ($SALOMEMECA_MEDCONVERTER_ROOT_DIR must be the same)
	@if [ "$(abspath $(PREFIX))" = "/usr" ] || \
			[ "$(abspath $(PREFIX))" = "/usr/local" ] || \
			[ "$(abspath $(PREFIX))" = "$(PWD)" ] ; then \
        echo "Can't uninstall automatically when PREFIX=$(PREFIX)"; \
		false ; \
	fi
	@echo -n "Are you sure you want to remove '$(PREFIX)/*' [y/n]? " ;
	@read verify ; [ "$$verify" = "y" ] || { echo "Interrupted!"; false ; }
	@rm -rf $(PREFIX)/*
	@rmdir $(PREFIX) 2> /dev/null || true

clean: ## Remove Python cache files
	@rm -f $$(find . -name '*.pyc')
	@rm -rf $$(find . -type d -name __pycache__) 2> /dev/null || true
	@rm -rf /tmp/_med_convert_cache/

.DEFAULT_GOAL := help
