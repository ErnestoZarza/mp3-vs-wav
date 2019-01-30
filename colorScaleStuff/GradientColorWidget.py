from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget, QPalette, QColor, QColorDialog
from colorScaleStuff.ui_gradientColorWidget import Ui_gradientColorWidget


class GradientColorWidget(QWidget, Ui_gradientColorWidget):

    colorChanged = pyqtSignal()

    def __init__(self, parent, isFirst=False, isLast=False):
        super(GradientColorWidget, self).__init__(parent)
        self.setupUi(self)

        self.isFirst = isFirst
        self.isLast = isLast

    @property
    def isLast(self):
        return self.posSpinBox.isReadOnly() and self.posSpinBox.value() == 0

    @isLast.setter
    def isLast(self, value):
        self.posSpinBox.setReadOnly(value)
        if value:
            self.posSpinBox.setValue(0)

    @property
    def isFirst(self):
        return self.posSpinBox.isReadOnly() and self.posSpinBox.value() == -120

    @isFirst.setter
    def isFirst(self, value):
        self.posSpinBox.setReadOnly(value)
        if value:
            self.posSpinBox.setValue(-120)

    def getTuple(self):
        pos = (self.posSpinBox.value() + 120) / 120.
        qcolor = self.colorLabel.palette().color(QPalette.Window)
        color = (qcolor.red(), qcolor.green(), qcolor.blue(), 255)
        return pos, color

    def applyTuple(self, t):
        self.setPos(t[0])
        self.setColor(t[1])

    def setColor(self, color):
        if type(color) == tuple:
            color = QColor(*color)

        palette = self.colorLabel.palette()
        palette.setColor(QPalette.Window, color)
        self.colorLabel.setPalette(palette)

    def setPos(self, value):
        self.posSpinBox.setValue(value*120 - 120)

    def mousePressEvent(self, QMouseEvent):
        if self.childAt(QMouseEvent.pos()) != self.colorLabel:
            return

        color = QColorDialog.getColor(self.colorLabel.palette().color(QPalette.Window), self)
        if color.isValid():
            self.setColor(color)
            self.colorChanged.emit()
