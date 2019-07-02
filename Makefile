SALOMEMECA_CONVMAIL_ROOT_DIR?=./convmail_installed
PREFIX=${SALOMEMECA_CONVMAIL_ROOT_DIR}
TRAD_DIR=resources/convmail

default: install

cleandir :
	make uninstall
	rm -rf $(TRAD_DIR)/ConvMail_msg_fr.qm

translate:
	pylupdate5 $(TRAD_DIR)/ConvMail.pro
	lrelease $(TRAD_DIR)/ConvMail.pro

install:
	make translate
	python setup.py install --prefix=$(PREFIX)
	python setup.py clean --all

uninstall :
	@if [ "$(abspath $(PREFIX))" = "/usr" ] || \
            [ "$(abspath $(PREFIX))" = "/usr/local" ] || \
            [ "$(abspath $(PREFIX))" = "$(PWD)" ] \
            ; then echo "Can't uninstall automatically when PREFIX=$(PREFIX)" ; false ; fi
	@echo -n "Are you sure you want to remove '$(PREFIX)/*' [y/n]? " ;
	@read verify ; [ "$$verify" = "y" ] || { echo "User aborted uninstall"; false ; }
	rm -rf $(PREFIX)/*
