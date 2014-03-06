# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'senses.ui'
#
# Created: Mon Sep  9 16:10:17 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Senses(object):
    def setupUi(self, Senses):
        Senses.setObjectName(_fromUtf8("Senses"))
        Senses.resize(400, 300)
        font = QtGui.QFont()
        font.setPointSize(12)
        Senses.setFont(font)
        self.horizontalLayoutWidget = QtGui.QWidget(Senses)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 391, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.ping = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ping.setFont(font)
        self.ping.setObjectName(_fromUtf8("ping"))
        self.horizontalLayout_2.addWidget(self.ping)
        self.nping = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.nping.setObjectName(_fromUtf8("nping"))
        self.horizontalLayout_2.addWidget(self.nping)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Senses)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 90, 391, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.sensores = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sensores.setFont(font)
        self.sensores.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sensores.setObjectName(_fromUtf8("sensores"))
        self.horizontalLayout_4.addWidget(self.sensores)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(Senses)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 120, 391, 80))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.iline = QtGui.QLCDNumber(self.horizontalLayoutWidget_3)
        self.iline.setObjectName(_fromUtf8("iline"))
        self.horizontalLayout_5.addWidget(self.iline)
        self.dline = QtGui.QLCDNumber(self.horizontalLayoutWidget_3)
        self.dline.setObjectName(_fromUtf8("dline"))
        self.horizontalLayout_5.addWidget(self.dline)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(Senses)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 200, 391, 80))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.medidor = QtGui.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.medidor.setFont(font)
        self.medidor.setObjectName(_fromUtf8("medidor"))
        self.horizontalLayout_6.addWidget(self.medidor)
        self.batery = QtGui.QLCDNumber(self.horizontalLayoutWidget_4)
        self.batery.setObjectName(_fromUtf8("batery"))
        self.horizontalLayout_6.addWidget(self.batery)

        self.retranslateUi(Senses)
        QtCore.QMetaObject.connectSlotsByName(Senses)

    def retranslateUi(self, Senses):
        Senses.setWindowTitle(QtGui.QApplication.translate("Senses", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.ping.setText(QtGui.QApplication.translate("Senses", "Ping", None, QtGui.QApplication.UnicodeUTF8))
        self.sensores.setText(QtGui.QApplication.translate("Senses", "Sensores de Línea", None, QtGui.QApplication.UnicodeUTF8))
        self.medidor.setText(QtGui.QApplication.translate("Senses", "Medidor de Batería", None, QtGui.QApplication.UnicodeUTF8))

