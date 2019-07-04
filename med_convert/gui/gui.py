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

import os.path as osp
import sys

from PyQt5 import Qt as Q

from ..utilities import translate
from .services import convert
from .settings import FileType, Settings
from .utilities import (connect, docs_path, get_dir_name, get_file_name,
                        resources_path, set_mandatory, to_list, update_palette)


class MainWindow(Q.QDialog):
    """
    Main window of *MedConvert* plugin.
    """

    def __init__(self, parent=None):
        """
        Create main window.

        Arguments:
            parent (Optional[QWidget]): Window's parent. Defaults to *None*.
        """
        super(MainWindow, self).__init__(parent)

        self._mandatory_ctrls = []

        self.setObjectName("med_convert_main_window")
        self.setModal(True)
        self.setAttribute(Q.Qt.WA_DeleteOnClose, True)

        title = translate("MedConvert",
                          "Mesh Converter")
        self.setWindowTitle(title)

        margin = 9
        spacing = 6

        # Create group-box for files description
        title = translate("MedConvert", "Files Selection")
        groupbox_files = Q.QGroupBox(title)

        # Create controls for output file parameter
        title = translate("MedConvert", "Output File")
        outputfile_label = Q.QLabel(groupbox_files)
        outputfile_label.setObjectName("outputfile_label")
        outputfile_label.setText(title)
        set_mandatory(outputfile_label)
        #--
        self.outputfile_edit = Q.QLineEdit(groupbox_files)
        self.outputfile_edit.setObjectName("outputfile_edit")
        self.outputfile_edit.setMinimumWidth(200)
        self.add_mandatory_ctrl(self.outputfile_edit)
        outputfile_label.setBuddy(self.outputfile_edit)
        #--
        title = translate("MedConvert", "Browse...")
        self.outputfile_btn = Q.QPushButton(groupbox_files)
        self.outputfile_btn.setObjectName("outputfile_btn")
        self.outputfile_btn.setText(title)

        # Create controls for input file parameter
        title = translate("MedConvert", "Input File")
        inputfile_label = Q.QLabel(groupbox_files)
        inputfile_label.setObjectName("inputfile_label")
        inputfile_label.setText(title)
        set_mandatory(inputfile_label)
        #--
        self.inputfile_edit = Q.QLineEdit(groupbox_files)
        self.inputfile_edit.setObjectName("inputfile_edit")
        self.inputfile_edit.setMinimumWidth(200)
        self.add_mandatory_ctrl(self.inputfile_edit)
        inputfile_label.setBuddy(self.inputfile_edit)
        #--
        title = translate("MedConvert", "Browse...")
        self.inputfile_btn = Q.QPushButton(groupbox_files)
        self.inputfile_btn.setObjectName("inputfile_btn")
        self.inputfile_btn.setText(title)

        # Lay out files controls
        grid_layout_files = Q.QGridLayout()
        grid_layout_files.setObjectName("grid_layout_files")
        grid_layout_files.setContentsMargins(margin, margin, margin, margin)

        grid_layout_files.addWidget(inputfile_label, 0, 0)
        grid_layout_files.addWidget(self.inputfile_edit, 0, 1)
        grid_layout_files.addWidget(self.inputfile_btn, 0, 2)

        grid_layout_files.addWidget(outputfile_label, 1, 0)
        grid_layout_files.addWidget(self.outputfile_edit, 1, 1)
        grid_layout_files.addWidget(self.outputfile_btn, 1, 2)

        grid_layout_files.setColumnStretch(1, 1)
        groupbox_files.setLayout(grid_layout_files)

        # Create group-box for launch conversion parameters
        title = translate("MedConvert", "Conversion Type")
        groupbox_conv = Q.QGroupBox(title)

        # Create controls for conversion_type choice
        #--
        title = FileType.value2str(FileType.SALOME_TO_SYSTUS)
        self.salome_to_systus_radio = Q.QRadioButton(groupbox_conv)
        self.salome_to_systus_radio.setObjectName("salome_to_systus_radio")
        self.salome_to_systus_radio.setText(title)
        #--
        title = FileType.value2str(FileType.SYSTUS_TO_SALOME)
        self.systus_to_salome_radio = Q.QRadioButton(groupbox_conv)
        self.systus_to_salome_radio.setObjectName("systus_to_salome_radio")
        self.systus_to_salome_radio.setText(title)
        #--
        self.conversion_type_group = Q.QButtonGroup(self)
        self.conversion_type_group.setExclusive(True)
        self.conversion_type_group.addButton(self.salome_to_systus_radio, FileType.SALOME_TO_SYSTUS)
        self.conversion_type_group.addButton(self.systus_to_salome_radio, FileType.SYSTUS_TO_SALOME)

        # Lay out launch calculation parameters
        vbox_layout_conv = Q.QVBoxLayout()
        vbox_layout_conv.setObjectName("vbox_layout_conv")
        vbox_layout_conv.setContentsMargins(margin, margin, margin, margin)
        vbox_layout_conv.addWidget(self.systus_to_salome_radio)
        vbox_layout_conv.addWidget(self.salome_to_systus_radio)
        groupbox_conv.setLayout(vbox_layout_conv)

        # Create horizontal separator to show above the buttons group
        separator = Q.QFrame()
        separator.setFrameShape(Q.QFrame.HLine)
        separator.setFrameShadow(Q.QFrame.Sunken)

        # Create Help button
        help_btn = Q.QPushButton(self)
        help_btn.setObjectName("help_btn")
        help_btn.setText(translate("MedConvert", "&Help"))

        # Create Launch button
        self._launch_btn = Q.QPushButton(self)
        self._launch_btn.setObjectName("launch_btn")
        self._launch_btn.setText(translate("MedConvert", "Launch"))

        # Create Close button
        close_btn = Q.QPushButton(self)
        close_btn.setObjectName("close_btn")
        close_btn.setText(translate("MedConvert", "&Close"))

        # Lay out buttons
        hbox_layout_btn = Q.QHBoxLayout()
        hbox_layout_btn.setObjectName("hbox_layout_btn")
        hbox_layout_btn.setContentsMargins(margin, margin, margin, margin)
        hbox_layout_btn.setSpacing(spacing)
        hbox_layout_btn.addWidget(help_btn)
        hbox_layout_btn.addStretch()
        hbox_layout_btn.addWidget(self._launch_btn)
        hbox_layout_btn.addStretch()
        hbox_layout_btn.addWidget(close_btn)

        # Lay out top-level widgets
        top_layout = Q.QGridLayout(self)
        top_layout.setObjectName("vbox_layout")
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(spacing)
        top_layout.addWidget(groupbox_files, 0, 2)
        top_layout.addWidget(groupbox_conv, 1, 2)
        top_layout.setRowMinimumHeight(2, 20)
        top_layout.setRowStretch(2, 1)
        top_layout.addWidget(separator, 3, 0, 1, 3)
        top_layout.addLayout(hbox_layout_btn, 4, 0, 1, 3)

        # # connections
        connect(self.outputfile_edit.textChanged, self.update_controls)
        connect(self.outputfile_btn.clicked, self.browse_file_out)
        connect(self.inputfile_edit.textChanged, self.update_controls)
        connect(self.inputfile_btn.clicked, self.browse_file_in)
        connect(self.conversion_type_group.buttonToggled, self.update_controls)
        connect(self._launch_btn.clicked, self.launch)
        connect(close_btn.clicked, self.reject)
        connect(help_btn.clicked, self.show_help)

        # initialize default values
        self.from_settings(Settings())

        # Update state
        self.update_controls()

    def from_settings(self, settings):
        """
        Update GUI controls from given settings.

        Arguments:
            settings (Settings): Settings object.
        """
        self.outputfile_edit.setText(settings.output_file)
        self.inputfile_edit.setText(settings.input_file)
        self.conversion_type_group.button(settings.conversion_type).setChecked(True)

    def to_settings(self):
        """
        Get settings from user input given in GUI controls.

        Returns:
            Settings: Settings object.
        """
        settings = Settings()

        settings.output_file = self.outputfile_edit.text()
        settings.input_file = self.inputfile_edit.text()
        settings.conversion_type = self.conversion_type_group.checkedId()
        return settings

    @Q.pyqtSlot()
    def show_help(self):
        """Called when user clicks *Help* button."""
        try:
            import SalomePyQt
            sg_pyqt = SalomePyQt.SalomePyQt()

            if docs_path():
                help_path = osp.join(docs_path(), 'index.html')
                sg_pyqt.helpContext(help_path, "")
                return
        except ImportError:
            pass
        title = translate("MedConvert", "Warning")
        message = translate("MedConvert", "Help is not available.")
        Q.QMessageBox.warning(self, title, message)


    @Q.pyqtSlot()
    def launch(self):
        """Called when user clicks *Launch* button."""

        current_settings = self.to_settings()
        current_settings.dump(sys.stdout)

        input_file = current_settings.input_file
        output_file = current_settings.output_file
        conversion_type = current_settings.conversion_type

        is_ok, msg = convert(input_file, output_file, conversion_type)

        if  is_ok:
            title = translate("MedConvert", "Information")
            message = translate("MedConvert",
                                "Conversion Done.")
            Q.QMessageBox.information(self, title, message)

        else:
            title = translate("MedConvert", "Error")
            message = translate("MedConvert",
                                "Conversion Failed.") + '\n%s'%msg
            Q.QMessageBox.critical(self, title, message)


    def reject(self):
        """
        Called when user presses *Escape* key or clicks *Cancel* or <X>(*Close*)
        button.
        """
        title = translate("MedConvert", "Exit")
        message = translate("MedConvert", "Are you sure you want to quit?")
        reply = Q.QMessageBox.question(self, title, message,
                                       Q.QMessageBox.Yes, Q.QMessageBox.No)
        if reply == Q.QMessageBox.Yes:
            super(MainWindow, self).reject()
            self.close()

    def update_controls(self):
        """Update dialog's widgets."""

        enable_launch_btn = True
        current_settings = self.to_settings()
        if not (current_settings.input_file and current_settings.output_file):
            enable_launch_btn = False

        self._launch_btn.setEnabled(enable_launch_btn)


    def browse_file_in(self):
        """Called when user presses *Browse* button to select a input file."""

        button = self.sender()
        edit_name = button.objectName().replace('btn', 'edit')
        edit = self.findChild(Q.QLineEdit, edit_name)

        title = translate("MedConvert", "Select a file")
        filters = []
        suffix = ""
        filters.append("Systus (*.ASC)")
        filters.append("Salome (*.med)")
        filters.append("All files (*)")
        file_name = get_file_name(self, 1, title, '', filters, suffix)
        if file_name:
            edit.setText(file_name)

    def browse_file_out(self):
        """Called when user presses *Browse* button to select a output file."""

        button = self.sender()
        edit_name = button.objectName().replace('btn', 'edit')
        edit = self.findChild(Q.QLineEdit, edit_name)

        title = translate("MedConvert", "Select a file")
        filters = []
        suffix = ""
        filters.append("Salome (*.med)")
        filters.append("All files (*)")
        file_name = get_file_name(self, 0, title, '', filters, suffix)
        if file_name:
            edit.setText(file_name)


    def add_mandatory_ctrl(self, ctrl):
        """
        Register given control as a mandatory one.

        Arguments:
            ctrl (QWidget): Control widget.
        """
        self._mandatory_ctrls.append(ctrl)


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
    language = context.sg.stringSetting('language', 'language') \
        if context is not None else 'en'
    parent = context.sg.getDesktop() \
        if context is not None else None

    translator = load_language(language)
    main_window = MainWindow(parent)
    translator.setParent(main_window)

    if context is not None:
        rect = context.sg.getDesktop().geometry()
    else:
        rect = Q.QApplication.desktop().availableGeometry()
    window_size = main_window.size()
    x_pos = max((rect.width() - window_size.width()) / 2, 0) + rect.x()
    y_pos = max((rect.height() - window_size.height()) / 2, 0) + rect.y()
    main_window.move(x_pos, y_pos)

    main_window.exec_()
