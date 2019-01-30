# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'discreteRangeColorWidget.ui'
#
# Created: Sat Aug 15 14:32:25 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_discreteRangeColorWidget(object):
    def setupUi(self, discreteRangeColorWidget):
        discreteRangeColorWidget.setObjectName(_fromUtf8("discreteRangeColorWidget"))
        discreteRangeColorWidget.resize(201, 20)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(discreteRangeColorWidget.sizePolicy().hasHeightForWidth())
        discreteRangeColorWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(discreteRangeColorWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lowerBoundSpinBox = QtGui.QSpinBox(discreteRangeColorWidget)
        self.lowerBoundSpinBox.setReadOnly(True)
        self.lowerBoundSpinBox.setMinimum(-120)
        self.lowerBoundSpinBox.setMaximum(0)
        self.lowerBoundSpinBox.setProperty("value", -120)
        self.lowerBoundSpinBox.setObjectName(_fromUtf8("lowerBoundSpinBox"))
        self.horizontalLayout.addWidget(self.lowerBoundSpinBox)
        self.upperBoundSpinBox = QtGui.QSpinBox(discreteRangeColorWidget)
        self.upperBoundSpinBox.setMinimum(-120)
        self.upperBoundSpinBox.setMaximum(0)
        self.upperBoundSpinBox.setObjectName(_fromUtf8("upperBoundSpinBox"))
        self.horizontalLayout.addWidget(self.upperBoundSpinBox)
        self.colorLabel = QtGui.QLabel(discreteRangeColorWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.colorLabel.setPalette(palette)
        self.colorLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.colorLabel.setAutoFillBackground(True)
        self.colorLabel.setText(_fromUtf8(""))
        self.colorLabel.setObjectName(_fromUtf8("colorLabel"))
        self.horizontalLayout.addWidget(self.colorLabel)

        self.retranslateUi(discreteRangeColorWidget)
        QtCore.QMetaObject.connectSlotsByName(discreteRangeColorWidget)

    def retranslateUi(self, discreteRangeColorWidget):
        discreteRangeColorWidget.setWindowTitle(QtGui.QApplication.translate("discreteRangeColorWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

