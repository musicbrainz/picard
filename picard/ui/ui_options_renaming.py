# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import (QtCore,
                   QtGui,
                   QtWidgets)


class Ui_RenamingOptionsPage(object):
    def setupUi(self, RenamingOptionsPage):
        RenamingOptionsPage.setObjectName("RenamingOptionsPage")
        RenamingOptionsPage.setEnabled(True)
        RenamingOptionsPage.resize(453, 540)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RenamingOptionsPage.sizePolicy().hasHeightForWidth())
        RenamingOptionsPage.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(RenamingOptionsPage)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.move_files = QtWidgets.QGroupBox(RenamingOptionsPage)
        self.move_files.setFlat(False)
        self.move_files.setCheckable(True)
        self.move_files.setChecked(False)
        self.move_files.setObjectName("move_files")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.move_files)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.move_files)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.move_files_to = QtWidgets.QLineEdit(self.move_files)
        self.move_files_to.setEnabled(False)
        self.move_files_to.setObjectName("move_files_to")
        self.horizontalLayout_4.addWidget(self.move_files_to)
        self.move_files_to_browse = QtWidgets.QPushButton(self.move_files)
        self.move_files_to_browse.setEnabled(False)
        self.move_files_to_browse.setObjectName("move_files_to_browse")
        self.horizontalLayout_4.addWidget(self.move_files_to_browse)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.move_additional_files = QtWidgets.QCheckBox(self.move_files)
        self.move_additional_files.setEnabled(False)
        self.move_additional_files.setObjectName("move_additional_files")
        self.verticalLayout_4.addWidget(self.move_additional_files)
        self.move_additional_files_pattern = QtWidgets.QLineEdit(self.move_files)
        self.move_additional_files_pattern.setEnabled(False)
        self.move_additional_files_pattern.setObjectName("move_additional_files_pattern")
        self.verticalLayout_4.addWidget(self.move_additional_files_pattern)
        self.delete_empty_dirs = QtWidgets.QCheckBox(self.move_files)
        self.delete_empty_dirs.setEnabled(False)
        self.delete_empty_dirs.setObjectName("delete_empty_dirs")
        self.verticalLayout_4.addWidget(self.delete_empty_dirs)
        self.verticalLayout_5.addWidget(self.move_files)
        self.rename_files = QtWidgets.QGroupBox(RenamingOptionsPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rename_files.sizePolicy().hasHeightForWidth())
        self.rename_files.setSizePolicy(sizePolicy)
        self.rename_files.setCheckable(True)
        self.rename_files.setChecked(False)
        self.rename_files.setObjectName("rename_files")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.rename_files)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ascii_filenames = QtWidgets.QCheckBox(self.rename_files)
        self.ascii_filenames.setObjectName("ascii_filenames")
        self.verticalLayout_3.addWidget(self.ascii_filenames)
        self.windows_compatibility = QtWidgets.QCheckBox(self.rename_files)
        self.windows_compatibility.setObjectName("windows_compatibility")
        self.verticalLayout_3.addWidget(self.windows_compatibility)
        self.file_naming_format_group = QtWidgets.QGroupBox(self.rename_files)
        self.file_naming_format_group.setObjectName("file_naming_format_group")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.file_naming_format_group)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.file_naming_format = QtWidgets.QTextEdit(self.file_naming_format_group)
        self.file_naming_format.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_naming_format.sizePolicy().hasHeightForWidth())
        self.file_naming_format.setSizePolicy(sizePolicy)
        self.file_naming_format.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.file_naming_format.setFont(font)
        self.file_naming_format.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.file_naming_format.setTabChangesFocus(False)
        self.file_naming_format.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.file_naming_format.setTabStopWidth(20)
        self.file_naming_format.setAcceptRichText(True)
        self.file_naming_format.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.file_naming_format.setObjectName("file_naming_format")
        self.verticalLayout_2.addWidget(self.file_naming_format)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.renaming_error = QtWidgets.QLabel(self.file_naming_format_group)
        self.renaming_error.setText("")
        self.renaming_error.setAlignment(QtCore.Qt.AlignCenter)
        self.renaming_error.setObjectName("renaming_error")
        self.horizontalLayout.addWidget(self.renaming_error)
        self.file_naming_format_default = QtWidgets.QPushButton(self.file_naming_format_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_naming_format_default.sizePolicy().hasHeightForWidth())
        self.file_naming_format_default.setSizePolicy(sizePolicy)
        self.file_naming_format_default.setMinimumSize(QtCore.QSize(0, 0))
        self.file_naming_format_default.setObjectName("file_naming_format_default")
        self.horizontalLayout.addWidget(self.file_naming_format_default)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.file_naming_format_group)
        self.file_naming_format_documentation = QtWidgets.QLabel(self.rename_files)
        self.file_naming_format_documentation.setText("")
        self.file_naming_format_documentation.setTextFormat(QtCore.Qt.RichText)
        self.file_naming_format_documentation.setWordWrap(True)
        self.file_naming_format_documentation.setOpenExternalLinks(True)
        self.file_naming_format_documentation.setObjectName("file_naming_format_documentation")
        self.verticalLayout_3.addWidget(self.file_naming_format_documentation)
        self.verticalLayout_5.addWidget(self.rename_files)
        self.groupBox = QtWidgets.QGroupBox(RenamingOptionsPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.example_filename = QtWidgets.QLabel(self.groupBox)
        self.example_filename.setText("")
        self.example_filename.setTextFormat(QtCore.Qt.RichText)
        self.example_filename.setWordWrap(True)
        self.example_filename.setObjectName("example_filename")
        self.verticalLayout.addWidget(self.example_filename)
        self.example_filename_va = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.example_filename_va.sizePolicy().hasHeightForWidth())
        self.example_filename_va.setSizePolicy(sizePolicy)
        self.example_filename_va.setText("")
        self.example_filename_va.setWordWrap(True)
        self.example_filename_va.setObjectName("example_filename_va")
        self.verticalLayout.addWidget(self.example_filename_va)
        self.verticalLayout_5.addWidget(self.groupBox)

        self.retranslateUi(RenamingOptionsPage)
        QtCore.QMetaObject.connectSlotsByName(RenamingOptionsPage)
        RenamingOptionsPage.setTabOrder(self.move_files, self.move_files_to)
        RenamingOptionsPage.setTabOrder(self.move_files_to, self.move_files_to_browse)
        RenamingOptionsPage.setTabOrder(self.move_files_to_browse, self.move_additional_files)
        RenamingOptionsPage.setTabOrder(self.move_additional_files, self.move_additional_files_pattern)
        RenamingOptionsPage.setTabOrder(self.move_additional_files_pattern, self.delete_empty_dirs)
        RenamingOptionsPage.setTabOrder(self.delete_empty_dirs, self.rename_files)
        RenamingOptionsPage.setTabOrder(self.rename_files, self.ascii_filenames)
        RenamingOptionsPage.setTabOrder(self.ascii_filenames, self.windows_compatibility)
        RenamingOptionsPage.setTabOrder(self.windows_compatibility, self.file_naming_format)
        RenamingOptionsPage.setTabOrder(self.file_naming_format, self.file_naming_format_default)

    def retranslateUi(self, RenamingOptionsPage):
        _translate = QtCore.QCoreApplication.translate
        self.move_files.setTitle(_("Move files when saving"))
        self.label.setText(_("Destination directory:"))
        self.move_files_to_browse.setText(_("Browse..."))
        self.move_additional_files.setText(_("Move additional files (case insensitive):"))
        self.delete_empty_dirs.setText(_("Delete empty directories"))
        self.rename_files.setTitle(_("Rename files when saving"))
        self.ascii_filenames.setText(_("Replace non-ASCII characters"))
        self.windows_compatibility.setText(_("Windows compatibility"))
        self.file_naming_format_group.setTitle(_("Name files like this"))
        self.file_naming_format.setHtml(_translate("RenamingOptionsPage",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'Monospace\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                   "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.file_naming_format_default.setText(_("Default"))
        self.groupBox.setTitle(_("Examples"))
