# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\\main\\python\\ui\\settings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(412, 206)
        Dialog.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 160, 371, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.clientpath = QtWidgets.QLineEdit(Dialog)
        self.clientpath.setGeometry(QtCore.QRect(20, 50, 301, 21))
        self.clientpath.setObjectName("clientpath")
        self.browse_button = QtWidgets.QPushButton(Dialog)
        self.browse_button.setGeometry(QtCore.QRect(330, 50, 61, 21))
        self.browse_button.setObjectName("browse_button")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 181, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 181, 16))
        self.label_2.setObjectName("label_2")
        self.autocomplete = QtWidgets.QComboBox(Dialog)
        self.autocomplete.setGeometry(QtCore.QRect(170, 121, 221, 21))
        self.autocomplete.setObjectName("autocomplete")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 91, 81, 16))
        self.label_3.setObjectName("label_3")
        self.yearprefix = QtWidgets.QLineEdit(Dialog)
        self.yearprefix.setGeometry(QtCore.QRect(170, 90, 221, 21))
        self.yearprefix.setObjectName("yearprefix")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.browse_button.setText(_translate("Dialog", "Browse"))
        self.label.setText(_translate("Dialog", "Set Client File Directory"))
        self.label_2.setText(_translate("Dialog", "Auto Complete Settings"))
        self.label_3.setText(_translate("Dialog", "Year Prefix"))

