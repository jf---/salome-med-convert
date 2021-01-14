# Copy/paste the first lines to generate the list of source files
#
# find ../../gui/ -name '*.ui' | sort | sed 's#^\.#FORMS += .#g'
# find ../../gui/ -name '*.py' | sort | grep -v Ui/ | sed 's#^\.#SOURCES += .#g'
# cd ..
#
# Create/update the .ts files with:
# pylupdate5 medconverter.pro
# linguist  medconverter_msg_fr.ts
# lrelease medconverter.pro

TRANSLATIONS += medconverter_msg_fr.ts

CODECFORTR = utf-8

FORMS += MainDialog.ui
SOURCES += ../../medconverter/utilities.py
SOURCES += ../../medconverter/gui/gui.py
SOURCES += ../../medconverter/gui/__init__.py
SOURCES += ../../medconverter/gui/settings.py
SOURCES += ../../medconverter/gui/utilities.py
