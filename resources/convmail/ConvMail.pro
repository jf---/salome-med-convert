# Copy/paste the first lines to generate the list of source files
#
# find ../../gui/ -name '*.ui' | sort | sed 's#^\.#FORMS += .#g' 
# find ../../gui/ -name '*.py' | sort | grep -v Ui/ | sed 's#^\.#SOURCES += .#g'
# cd ..
#
# Create/update the .ts files with:
# pylupdate5 ConvMail.pro
# linguist  ConvMail_msg_fr.ts
# lrelease ConvMail.pro

TRANSLATIONS += ConvMail_msg_fr.ts

CODECFORTR = utf-8

SOURCES += ../../convmail/utilities.py
SOURCES += ../../convmail/gui/gui.py
SOURCES += ../../convmail/gui/__init__.py
SOURCES += ../../convmail/gui/services.py
SOURCES += ../../convmail/gui/settings.py
SOURCES += ../../convmail/gui/utilities.py
SOURCES += ../../salome_plugins.py

