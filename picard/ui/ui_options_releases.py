# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import (QtCore,
                   QtWidgets)


class Ui_ReleasesOptionsPage(object):
    def setupUi(self, ReleasesOptionsPage):
        ReleasesOptionsPage.setObjectName("ReleasesOptionsPage")
        ReleasesOptionsPage.resize(551, 497)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ReleasesOptionsPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.type_group = QtWidgets.QGroupBox(ReleasesOptionsPage)
        self.type_group.setObjectName("type_group")
        self.gridLayout = QtWidgets.QGridLayout(self.type_group)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3.addWidget(self.type_group)
        self.country_group = QtWidgets.QGroupBox(ReleasesOptionsPage)
        self.country_group.setObjectName("country_group")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.country_group)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.country_list = QtWidgets.QListWidget(self.country_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.country_list.sizePolicy().hasHeightForWidth())
        self.country_list.setSizePolicy(sizePolicy)
        self.country_list.setObjectName("country_list")
        self.horizontalLayout.addWidget(self.country_list)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.add_countries = QtWidgets.QPushButton(self.country_group)
        self.add_countries.setObjectName("add_countries")
        self.verticalLayout.addWidget(self.add_countries)
        self.remove_countries = QtWidgets.QPushButton(self.country_group)
        self.remove_countries.setObjectName("remove_countries")
        self.verticalLayout.addWidget(self.remove_countries)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.preferred_country_list = QtWidgets.QListWidget(self.country_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preferred_country_list.sizePolicy().hasHeightForWidth())
        self.preferred_country_list.setSizePolicy(sizePolicy)
        self.preferred_country_list.setDragEnabled(True)
        self.preferred_country_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.preferred_country_list.setObjectName("preferred_country_list")
        self.horizontalLayout.addWidget(self.preferred_country_list)
        self.verticalLayout_3.addWidget(self.country_group)
        self.format_group = QtWidgets.QGroupBox(ReleasesOptionsPage)
        self.format_group.setObjectName("format_group")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.format_group)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.format_list = QtWidgets.QListWidget(self.format_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.format_list.sizePolicy().hasHeightForWidth())
        self.format_list.setSizePolicy(sizePolicy)
        self.format_list.setObjectName("format_list")
        self.horizontalLayout_2.addWidget(self.format_list)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.add_formats = QtWidgets.QPushButton(self.format_group)
        self.add_formats.setObjectName("add_formats")
        self.verticalLayout_2.addWidget(self.add_formats)
        self.remove_formats = QtWidgets.QPushButton(self.format_group)
        self.remove_formats.setObjectName("remove_formats")
        self.verticalLayout_2.addWidget(self.remove_formats)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.preferred_format_list = QtWidgets.QListWidget(self.format_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preferred_format_list.sizePolicy().hasHeightForWidth())
        self.preferred_format_list.setSizePolicy(sizePolicy)
        self.preferred_format_list.setDragEnabled(True)
        self.preferred_format_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.preferred_format_list.setObjectName("preferred_format_list")
        self.horizontalLayout_2.addWidget(self.preferred_format_list)
        self.verticalLayout_3.addWidget(self.format_group)

        self.retranslateUi(ReleasesOptionsPage)
        QtCore.QMetaObject.connectSlotsByName(ReleasesOptionsPage)

    def retranslateUi(self, ReleasesOptionsPage):
        _translate = QtCore.QCoreApplication.translate
        self.type_group.setTitle(_("Preferred release types"))
        self.country_group.setTitle(_("Preferred release countries"))
        self.add_countries.setText(_(">"))
        self.remove_countries.setText(_("<"))
        self.format_group.setTitle(_("Preferred release formats"))
        self.add_formats.setText(_(">"))
        self.remove_formats.setText(_("<"))
