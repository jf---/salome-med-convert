# Copy/paste the first lines to generate the list of source files
#
# find ../../gui/ -name '*.ui' | sort | sed 's#^\.#FORMS += .#g'
# find ../../gui/ -name '*.py' | sort | grep -v Ui/ | sed 's#^\.#SOURCES += .#g'
# cd ..
#
# Create/update the .ts files with:
# pylupdate5 MedConvert.pro
# linguist  MedConvert_msg_fr.ts
# lrelease MedConvert.pro

TRANSLATIONS += MedConvert_msg_fr.ts

CODECFORTR = utf-8

SOURCES += ../../med_convert/utilities.py
SOURCES += ../../med_convert/gui/gui.py
SOURCES += ../../med_convert/gui/__init__.py
SOURCES += ../../med_convert/gui/services.py
SOURCES += ../../med_convert/gui/settings.py
SOURCES += ../../med_convert/gui/utilities.py
SOURCES += ../../salome_plugins.py
