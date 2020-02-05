# -*- coding: utf-8 -*-

# Copyright 2018 EDF R&D
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, you may download a copy of license
# from https://www.gnu.org/licenses/gpl-3.0.

"""
Implementation of Graphical User Interface for *MedConvert* plugin.
"""

import os
import os.path as osp
import sys
import tempfile
import traceback

from PyQt5 import Qt as Q
from PyQt5 import QtCore, uic

from . import supported_input_formats, supported_output_formats, convert
from ..convert import Fmt
from ..utilities import HAS_SALOME, translate
from .settings import Settings
from .utilities import (connect, docs_path, get_dir_name, get_file_name,
                        publish_meshes, resources_path, to_list)

UIFILE = osp.join(resources_path(), "med_convert", "MainDialog.ui")
BASE, FORM = uic.loadUiType(UIFILE)


class MainDialog(BASE, FORM):

    """
    Main window of *MedConvert* plugin.
    """

    def __init__(self, parent=None):
        """
        Create main window.

        Arguments:
            parent (Optional[QWidget]): Window's parent. Defaults to *None*.
        """
        super().__init__(parent)
        self.setupUi(self)

        title = translate("MedConvert",
                          "Mesh Converter")
        self.setWindowTitle(title)
        self.setStatus("")

        self.applyButton.setText(translate("MedConvert", "Apply"))      
        self.closeButton.setText(translate("MedConvert", "Close"))      
        self.helpButton.setText(translate("MedConvert", "Help"))      
        self.inFileLineEditLabel.setText(translate("MedConvert", "Input mesh file"))      
        self.inFormatBoxLabel.setText(translate("MedConvert", "Input mesh format"))      
        self.outFileCheckBox.setText(translate("MedConvert", "Output MED file"))      
        self.smeshCheckBox.setText(translate("MedConvert", "Import mesh in SMESH"))           

        self.smeshCheckBox.setEnabled(HAS_SALOME)
        if not HAS_SALOME:
            self.outFileCheckBox.setChecked(True)
            self.smeshCheckBox.setText(self.smeshCheckBox.text()
                                       + " (SALOME is not available)")
        connect(self.inFileLineEdit.textChanged, self.update_controls)
        connect(self.inFileButton.clicked, self.browse_file_in)
        connect(self.inFormatBox.currentIndexChanged, self.update_controls)
        connect(self.outFileCheckBox.stateChanged, self.update_controls)
        connect(self.outFileLineEdit.textChanged, self.update_controls)
        connect(self.outFileButton.clicked, self.browse_file_out)
        connect(self.smeshCheckBox.stateChanged, self.update_controls)
        connect(self.applyButton.clicked, self.launch)
        connect(self.closeButton.clicked, self.close)
        connect(self.helpButton.clicked, self.show_help)

        self.inFormatBox.addItems([Fmt.name(i) for i in supported_input_formats()])

        # initialize default values
        self.from_settings(Settings())

        # Update state
        self.update_controls()

    def setStatus(self, text, color="#ff0000"):
        """Set the text of the status line.

        Arguments:
            text (str): Text to be shown.
        """
        self.statusText.setText("<font color='{1}'><i>{0}</i></font>"
                                .format(text, color))

    def from_settings(self, settings):
        """
        Update GUI controls from given settings.

        Arguments:
            settings (Settings): Settings object.
        """
        self.outFileLineEdit.setText(settings.output_file)
        self.inFileLineEdit.setText(settings.input_file)
        self.inFormatBox.setCurrentText(Fmt.name(settings.input_format))


    def to_settings(self):
        """
        Get settings from user input given in GUI controls.

        Returns:
            Settings: Settings object.
        """
        settings = Settings()

        settings.output_file = self.outFileLineEdit.text()
        settings.input_file = self.inFileLineEdit.text()
        settings.input_format = Fmt.get(self.inFormatBox.currentText())
        
        return settings

    @Q.pyqtSlot()
    def show_help(self):
        """Called when user clicks *Help* button."""
        if not docs_path():
            title = translate("MedConvert", "Warning")
            message = translate("MedConvert", "Help is not available.")
            Q.QMessageBox.warning(self, title, message)
            return

        url = osp.join(docs_path(), 'index.html')
        Q.QDesktopServices.openUrl(Q.QUrl(url))

    @Q.pyqtSlot()
    def launch(self):
        """Called when user clicks *Apply* button."""
        self.setStatus(translate('MedConvert',
                                 'Converting mesh, please wait...'),
                       color='#0000ff')
        QtCore.QTimer.singleShot(50, self.do_convert)

    def do_convert(self):
        """Execute the mesh conversion."""
        settings = self.to_settings()
        use_tmp = False
        if not settings.output_file:
            use_tmp = True
            settings.output_file = tempfile.mkstemp(suffix=".med")[1]
        settings.dump(sys.stdout)

        verbose = int(os.getenv("DEBUG", 0))
        is_ok, err = convert(settings.input_file, settings.input_format,
                             settings.output_file, settings.output_format, verbose)
        self.setStatus("")

        if is_ok:
            if self.smeshCheckBox.isChecked():
                publish_meshes(settings.output_file)
                self.setStatus(translate('MedConvert',
                                         "Open the SMESH module and refresh "
                                         "(F5) the object browser<br/>"
                                         "to see the newly created mesh."),
                            color='#0000ff')
                if use_tmp:
                    os.remove(settings.output_file)

            title = translate("MedConvert", "Information")
            message = translate("MedConvert",
                                "Conversion Done.")
            Q.QMessageBox.information(self, title, message)

        else:
            mbox = Q.QMessageBox()
            mbox.setWindowTitle(translate("MedConvert", "Error"))
            mbox.setIcon(Q.QMessageBox.Critical)
            mbox.setText(translate("MedConvert",
                                   "Conversion Failed.\n{0}").format(err))
            mbox.setDetailedText("".join(
                traceback.format_tb(err.__traceback__)))
            mbox.exec_()

    def update_controls(self):
        """Update dialog's widgets."""
        
        self.applyButton.setEnabled(self.is_valid())
        self.inFileLineEdit.setEnabled(self.inFormatBox.currentIndex())
        self.inFileButton.setEnabled(self.inFormatBox.currentIndex())
        self.outFileLineEdit.setEnabled(self.outFileCheckBox.isChecked())
        self.outFileButton.setEnabled(self.outFileCheckBox.isChecked())

    def is_valid(self):
        """Tell if the settings are valid, the conversion can be launched.

        Returns:
            bool: *True* if the required data are set, *False* otherwise.
        """
        settings = self.to_settings()

        if settings.input_format == Fmt.Null :
            self.setStatus(translate('MedConvert',
                                     'Please select the input mesh format.'))
            return False
            
        if not settings.input_file:
            self.setStatus(translate('MedConvert',
                                     'Please select the input mesh file.'))
            return False
        if not (self.outFileCheckBox.isChecked()
                or self.smeshCheckBox.isChecked()):
            self.setStatus(translate('MedConvert',
                                     'Please select at least one output type.'))
            return False
        if self.outFileCheckBox.isChecked() and not settings.output_file:
            self.setStatus(translate('MedConvert',
                                     'Please select the output file.'))
            return False
        self.setStatus("")
        return True

    def browse_file_in(self):
        """Called when user presses *Browse* button to select a input file."""

        title = translate("MedConvert", "Select a file")
        filters = []

        settings = self.to_settings()
        ext = Fmt.extensions(settings.input_format)
        filters.append('%s (%s)'%(Fmt.name(settings.input_format), ' '.join(('*%s'%i for i in ext))))
        filters.append("All files (*)")

        suffix = ""
        file_name = get_file_name(self, 1, title, '', filters, suffix)
        if file_name:
            self.inFileLineEdit.setText(file_name)

    def browse_file_out(self):
        """Called when user presses *Browse* button to select a output file."""

        title = translate("MedConvert", "Select a file")
        filters = []

        settings = self.to_settings()
        ext = Fmt.extensions(settings.output_format)
        filters.append('%s (%s)'%(Fmt.name(settings.output_format), ' '.join(('*%s'%i for i in ext))))
        filters.append("All files (*)")

        suffix = ""
        file_name = get_file_name(self, 0, title, '', filters, suffix)
        if file_name:
            self.outFileLineEdit.setText(file_name)


def load_language(language='en'):
    """
    Load translators for specified language.

    Arguments:
        language (Optional[str]): Language to use. Defaults to 'en' (English).
    """
    qobject = Q.QObject()

    # Load Qt translations
    qt_translations_dir = \
        Q.QLibraryInfo.location(Q.QLibraryInfo.TranslationsPath)
    for qt_tr in ('qt', 'qtbase'):
        translator = Q.QTranslator(qobject)
        if translator.load(qt_tr + '_%s' % language, qt_translations_dir):
            Q.QApplication.instance().installTranslator(translator)

    # Load plugin translations
    translator = Q.QTranslator(qobject)
    if translator.load('MedConvert_msg_{}'.format(language),
                       osp.join(resources_path(), 'med_convert')):
        Q.QApplication.instance().installTranslator(translator)

    return qobject


def start(context=None):
    """
    Show main window of *MedConvert* plugin.

    Arguments:
        context: SALOME GUI context.
    """
    if context:
        lang = context.sg.stringSetting('language', 'language')
        parent = context.sg.getDesktop()
    else:
        # create application
        app = Q.QApplication(sys.argv)
        app.lastWindowClosed.connect(app.quit)
        lang = 'en' if not 'fr' in Q.QLocale.system().name() else 'fr'
        parent = None

    parent = context.sg.getDesktop() \
        if context is not None else None

    translator = load_language(lang)
    main_window = MainDialog(parent)
    translator.setParent(main_window)

    main_window.exec_()
