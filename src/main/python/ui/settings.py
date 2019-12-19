# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\\main\python\\ui\\settings.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(548, 233)
        Dialog.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.browse_button_wp = QtWidgets.QPushButton(self.frame)
        self.browse_button_wp.setObjectName("browse_button_wp")
        self.gridLayout.addWidget(self.browse_button_wp, 2, 3, 1, 1)
        self.yearprefix = QtWidgets.QLineEdit(self.frame)
        self.yearprefix.setObjectName("yearprefix")
        self.gridLayout.addWidget(self.yearprefix, 9, 1, 1, 1)
        self.wptemplate = QtWidgets.QLineEdit(self.frame)
        self.wptemplate.setObjectName("wptemplate")
        self.gridLayout.addWidget(self.wptemplate, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 10, 0, 1, 1)
        self.wpfolder = QtWidgets.QLineEdit(self.frame)
        self.wpfolder.setObjectName("wpfolder")
        self.gridLayout.addWidget(self.wpfolder, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.clientpath = QtWidgets.QLineEdit(self.frame)
        self.clientpath.setObjectName("clientpath")
        self.gridLayout.addWidget(self.clientpath, 0, 1, 1, 1)
        self.browse_button = QtWidgets.QPushButton(self.frame)
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 9, 0, 1, 1)
        self.autocomplete = QtWidgets.QComboBox(self.frame)
        self.autocomplete.setObjectName("autocomplete")
        self.gridLayout.addWidget(self.autocomplete, 10, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 14, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 15, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 14, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.browse_button_wp.setText(_translate("Dialog", "Browse"))
        self.label_2.setText(_translate("Dialog", "Auto Complete Settings"))
        self.label.setText(_translate("Dialog", "Set Client File Directory"))
        self.label_5.setText(_translate("Dialog", "Workpaper Folder Name"))
        self.browse_button.setText(_translate("Dialog", "Browse"))
        self.label_4.setText(_translate("Dialog", "Workpaper Template Path"))
        self.label_3.setText(_translate("Dialog", "Year Prefix"))
        self.label_6.setText(_translate("Dialog", "Tab Preference"))
