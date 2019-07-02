SALOMEMECA_MED_CONVERT_ROOT_DIR ?= ./install
PREFIX = ${SALOMEMECA_MED_CONVERT_ROOT_DIR}
TRAD_DIR = resources/med_convert

default: install

translate:
	pylupdate5 $(TRAD_DIR)/MedConvert.pro
	lrelease $(TRAD_DIR)/MedConvert.pro

install:
	make translate
	python setup.py install --prefix=$(PREFIX)
	python setup.py clean --all

uninstall:
	@if [ "$(abspath $(PREFIX))" = "/usr" ] || \
            [ "$(abspath $(PREFIX))" = "/usr/local" ] || \
            [ "$(abspath $(PREFIX))" = "$(PWD)" ] \
            ; then echo "Can't uninstall automatically when PREFIX=$(PREFIX)" ; false ; fi
	@echo -n "Are you sure you want to remove '$(PREFIX)/*' [y/n]? " ;
	@read verify ; [ "$$verify" = "y" ] || { echo "User aborted uninstall"; false ; }
	rm -rf $(PREFIX)/*

clean:
	@rm -f $$(find . -name '*.pyc')
	@rmdir $$(find . -type d) 2> /dev/null || true

distclean:
	rm -f $(TRAD_DIR)/MedConvert_msg_fr.qm
	make uninstall
