# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/options_cover.ui'
#
# Created: Thu Jan 24 08:40:53 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CoverOptionsPage(object):
    def setupUi(self, CoverOptionsPage):
        CoverOptionsPage.setObjectName(_fromUtf8("CoverOptionsPage"))
        CoverOptionsPage.resize(525, 522)
        self.verticalLayout = QtGui.QVBoxLayout(CoverOptionsPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rename_files = QtGui.QGroupBox(CoverOptionsPage)
        self.rename_files.setObjectName(_fromUtf8("rename_files"))
        self.vboxlayout = QtGui.QVBoxLayout(self.rename_files)
        self.vboxlayout.setSpacing(2)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.save_images_to_tags = QtGui.QCheckBox(self.rename_files)
        self.save_images_to_tags.setObjectName(_fromUtf8("save_images_to_tags"))
        self.vboxlayout.addWidget(self.save_images_to_tags)
        self.cb_embed_front_only = QtGui.QCheckBox(self.rename_files)
        self.cb_embed_front_only.setObjectName(_fromUtf8("cb_embed_front_only"))
        self.vboxlayout.addWidget(self.cb_embed_front_only)
        self.save_images_to_files = QtGui.QCheckBox(self.rename_files)
        self.save_images_to_files.setObjectName(_fromUtf8("save_images_to_files"))
        self.vboxlayout.addWidget(self.save_images_to_files)
        self.label_3 = QtGui.QLabel(self.rename_files)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.vboxlayout.addWidget(self.label_3)
        self.cover_image_filename = QtGui.QLineEdit(self.rename_files)
        self.cover_image_filename.setObjectName(_fromUtf8("cover_image_filename"))
        self.vboxlayout.addWidget(self.cover_image_filename)
        self.save_images_overwrite = QtGui.QCheckBox(self.rename_files)
        self.save_images_overwrite.setObjectName(_fromUtf8("save_images_overwrite"))
        self.vboxlayout.addWidget(self.save_images_overwrite)
        self.verticalLayout.addWidget(self.rename_files)
        self.groupBox = QtGui.QGroupBox(CoverOptionsPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.caprovider_caa = QtGui.QCheckBox(self.groupBox)
        self.caprovider_caa.setObjectName(_fromUtf8("caprovider_caa"))
        self.verticalLayout_2.addWidget(self.caprovider_caa)
        self.caprovider_amazon = QtGui.QCheckBox(self.groupBox)
        self.caprovider_amazon.setObjectName(_fromUtf8("caprovider_amazon"))
        self.verticalLayout_2.addWidget(self.caprovider_amazon)
        self.caprovider_cdbaby = QtGui.QCheckBox(self.groupBox)
        self.caprovider_cdbaby.setObjectName(_fromUtf8("caprovider_cdbaby"))
        self.verticalLayout_2.addWidget(self.caprovider_cdbaby)
        self.caprovider_whitelist = QtGui.QCheckBox(self.groupBox)
        self.caprovider_whitelist.setObjectName(_fromUtf8("caprovider_whitelist"))
        self.verticalLayout_2.addWidget(self.caprovider_whitelist)
        self.verticalLayout.addWidget(self.groupBox)
        self.gb_caa = QtGui.QGroupBox(CoverOptionsPage)
        self.gb_caa.setEnabled(False)
        self.gb_caa.setObjectName(_fromUtf8("gb_caa"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gb_caa)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.gb_caa)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cb_image_size = QtGui.QComboBox(self.gb_caa)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_image_size.sizePolicy().hasHeightForWidth())
        self.cb_image_size.setSizePolicy(sizePolicy)
        self.cb_image_size.setObjectName(_fromUtf8("cb_image_size"))
        self.cb_image_size.addItem(_fromUtf8(""))
        self.cb_image_size.addItem(_fromUtf8(""))
        self.cb_image_size.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.cb_image_size)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_2 = QtGui.QLabel(self.gb_caa)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.le_image_types = QtGui.QLineEdit(self.gb_caa)
        self.le_image_types.setObjectName(_fromUtf8("le_image_types"))
        self.verticalLayout_3.addWidget(self.le_image_types)
        self.caa_types_help = QtGui.QLabel(self.gb_caa)
        self.caa_types_help.setObjectName(_fromUtf8("caa_types_help"))
        self.verticalLayout_3.addWidget(self.caa_types_help)
        self.cb_approved_only = QtGui.QCheckBox(self.gb_caa)
        self.cb_approved_only.setObjectName(_fromUtf8("cb_approved_only"))
        self.verticalLayout_3.addWidget(self.cb_approved_only)
        self.cb_type_as_filename = QtGui.QCheckBox(self.gb_caa)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_type_as_filename.sizePolicy().hasHeightForWidth())
        self.cb_type_as_filename.setSizePolicy(sizePolicy)
        self.cb_type_as_filename.setObjectName(_fromUtf8("cb_type_as_filename"))
        self.verticalLayout_3.addWidget(self.cb_type_as_filename)
        self.verticalLayout.addWidget(self.gb_caa)
        spacerItem1 = QtGui.QSpacerItem(275, 91, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(CoverOptionsPage)
        QtCore.QObject.connect(self.save_images_to_tags, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.cb_embed_front_only.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(CoverOptionsPage)
        CoverOptionsPage.setTabOrder(self.save_images_to_tags, self.save_images_to_files)
        CoverOptionsPage.setTabOrder(self.save_images_to_files, self.cover_image_filename)

    def retranslateUi(self, CoverOptionsPage):
        self.rename_files.setTitle(_("Location"))
        self.save_images_to_tags.setText(_("Embed cover images into tags"))
        self.cb_embed_front_only.setText(_("Embed only front images"))
        self.save_images_to_files.setText(_("Save cover images as separate files"))
        self.label_3.setText(_("Use the following file name for images:"))
        self.save_images_overwrite.setText(_("Overwrite the file if it already exists"))
        self.groupBox.setTitle(_("Coverart Providers"))
        self.caprovider_caa.setText(_("Cover Art Archive"))
        self.caprovider_amazon.setText(_("Amazon"))
        self.caprovider_cdbaby.setText(_("CD Baby"))
        self.caprovider_whitelist.setText(_("Sites on the whitelist"))
        self.gb_caa.setTitle(_("Cover Art Archive"))
        self.label.setText(_("Only use images of the following size:"))
        self.cb_image_size.setItemText(0, _("250 px"))
        self.cb_image_size.setItemText(1, _("500 px"))
        self.cb_image_size.setItemText(2, _("Full size"))
        self.label_2.setText(_("Download only images of the following types:"))
        self.caa_types_help.setText(_("Types are separated by spaces, and are not case-sensitive."))
        self.cb_approved_only.setText(_("Download only approved images"))
        self.cb_type_as_filename.setText(_("Use the first image type as the filename. This will not change the filename of front images."))

