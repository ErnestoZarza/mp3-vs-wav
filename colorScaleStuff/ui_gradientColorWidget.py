# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gradientColorWidget.ui'
#
# Created: Sun Aug 16 00:48:14 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_gradientColorWidget(object):
    def setupUi(self, gradientColorWidget):
        gradientColorWidget.setObjectName(_fromUtf8("gradientColorWidget"))
        gradientColorWidget.resize(144, 20)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(gradientColorWidget.sizePolicy().hasHeightForWidth())
        gradientColorWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(gradientColorWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.posSpinBox = QtGui.QSpinBox(gradientColorWidget)
        self.posSpinBox.setMinimum(-120)
        self.posSpinBox.setMaximum(0)
        self.posSpinBox.setObjectName(_fromUtf8("posSpinBox"))
        self.horizontalLayout.addWidget(self.posSpinBox)
        self.colorLabel = QtGui.QLabel(gradientColorWidget)
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

        self.retranslateUi(gradientColorWidget)
        QtCore.QMetaObject.connectSlotsByName(gradientColorWidget)

    def retranslateUi(self, gradientColorWidget):
        gradientColorWidget.setWindowTitle(QtGui.QApplication.translate("gradientColorWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

