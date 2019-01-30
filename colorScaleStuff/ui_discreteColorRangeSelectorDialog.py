# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'discreteColorRangeSelectorDialog.ui'
#
# Created: Sat Aug 15 16:13:06 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_discreteColorRangeSelector(object):
    def setupUi(self, discreteColorRangeSelector):
        discreteColorRangeSelector.setObjectName(_fromUtf8("discreteColorRangeSelector"))
        discreteColorRangeSelector.resize(267, 300)
        self.verticalLayout = QtGui.QVBoxLayout(discreteColorRangeSelector)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(discreteColorRangeSelector)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 247, 251))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttonBox = QtGui.QDialogButtonBox(discreteColorRangeSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(discreteColorRangeSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), discreteColorRangeSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), discreteColorRangeSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(discreteColorRangeSelector)

    def retranslateUi(self, discreteColorRangeSelector):
        discreteColorRangeSelector.setWindowTitle(QtGui.QApplication.translate("discreteColorRangeSelector", "Select Colors", None, QtGui.QApplication.UnicodeUTF8))

