from PyQt4.QtGui import QWidget, QPalette, QColor, QColorDialog

from colorScaleStuff.ui_discreteColorWidget import Ui_discreteRangeColorWidget
from widgets import utils


class DiscreteRangeColorWidget(QWidget, Ui_discreteRangeColorWidget):
    def __init__(self, parent, previous, isLast=False):
        super(DiscreteRangeColorWidget, self).__init__(parent)
        self.setupUi(self)

        self.isLast = isLast
        self.previous = previous

        self.utils = utils.utils()

    @property
    def isLast(self):
        return self.upperBoundSpinBox.isReadOnly()

    @isLast.setter
    def isLast(self, value):
        self.upperBoundSpinBox.setReadOnly(value)
        if value:
            self.upperBoundSpinBox.setValue(0)

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, value):
        self._previous = value
        if value is not None:
            self._previous.upperBoundSpinBox.valueChanged.connect(self.lowerBoundSpinBox.setValue)

    @property
    def isFirst(self):
        return self.previous is None

    def getTuples(self):
        start = (self.lowerBoundSpinBox.value() + 120) / 120.
        end = (self.upperBoundSpinBox.value() + 120) / 120.
        qcolor = self.colorLabel.palette().color(QPalette.Window)
        color = (qcolor.red(), qcolor.green(), qcolor.blue(), 255)
        return [(start, color), (end, color)]

    def applyTuples(self, t_start, t_end):
        self.setStart(t_start[0] - self.utils.gradientEpsilon)
        self.setEnd(t_end[0])
        self.setColor(t_start[1])

    def setColor(self, color):
        if type(color) == tuple:
            color = QColor(*color)

        palette = self.colorLabel.palette()
        palette.setColor(QPalette.Window, color)
        self.colorLabel.setPalette(palette)

    def setStart(self, value):
        self.lowerBoundSpinBox.setValue(value*120 - 120)

    def setEnd(self, value):
        self.upperBoundSpinBox.setValue(value*120 - 120)

    def mousePressEvent(self, QMouseEvent):
        if self.childAt(QMouseEvent.pos()) != self.colorLabel:
            return

        color = QColorDialog.getColor(self.colorLabel.palette().color(QPalette.Window), self)
        if color.isValid():
            self.setColor(color)
