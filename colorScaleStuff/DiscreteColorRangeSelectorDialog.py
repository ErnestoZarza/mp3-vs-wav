from itertools import chain
import sys

from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import QDialog, QPushButton, QSizePolicy, QApplication, QHBoxLayout, QSpacerItem

from colorScaleStuff.DiscreteRangeColorWidget import DiscreteRangeColorWidget
from colorScaleStuff.ui_discreteColorRangeSelectorDialog import Ui_discreteColorRangeSelector
from widgets import utils


class DiscreteColorRangeSelectorDialog(QDialog, Ui_discreteColorRangeSelector):
    def __init__(self, parent=None, gradientTicks=None):
        if parent is not None:
            super(DiscreteColorRangeSelectorDialog, self).__init__(parent)
        else:
            super(DiscreteColorRangeSelectorDialog, self).__init__()

        self.setupUi(self)

        self.utils = utils.utils()

        if gradientTicks is None:
            gradientTicks = self.utils.defaultDiscreteColorGradientTicks

        self._rangeColorWidgets = []
        self._addButtons = []
        self._removeButtons = []
        self.applyGradientTicks(gradientTicks)

    def _insert_color_range_slot(self, index):
        gradientTicks = self.getGradientTicks()

        if not (0 < index < len(gradientTicks)/2):
            return

        # the new range takes the first half of the next range
        start = gradientTicks[index*2][0]
        end = (start-self.utils.gradientEpsilon + gradientTicks[index*2+1][0]) / 2.
        gradientTicks[index*2] = end + self.utils.gradientEpsilon, gradientTicks[index*2][1]

        # the new range's color is the mean color of the previous and next ranges
        color_prev = gradientTicks[index*2-1][1]
        color_next = gradientTicks[index*2][1]
        color = tuple((x1+x2)/2 for x1, x2 in zip(color_prev, color_next))

        gradientTicks.insert(index*2, (start, color))
        gradientTicks.insert(index*2+1, (end, color))

        self.applyGradientTicks(gradientTicks)

    def _remove_color_range_slot(self, index):
        gradientTicks = self.getGradientTicks()

        if len(gradientTicks) <= 4 or len(gradientTicks) < index*2+2:
            return

        if index > 0:
            gradientTicks[index*2 - 1] = gradientTicks[index*2 + 1][0], gradientTicks[index*2 - 1][1]
        else:
            gradientTicks[(index+1)*2] = 0, gradientTicks[(index+1)*2][1]

        gradientTicks = gradientTicks[:index*2] + gradientTicks[index*2+2:]

        self.applyGradientTicks(gradientTicks)

    def _add_drcWidget(self, index, gradientTicks, prevDRCWidget):
        drcw = DiscreteRangeColorWidget(self.scrollAreaWidgetContents, prevDRCWidget)
        rbtn = QPushButton(self.scrollAreaWidgetContents)
        hlayout = QHBoxLayout()

        self._rangeColorWidgets.append(drcw)
        self._removeButtons.append(rbtn)

        drcw.applyTuples(gradientTicks[index*2], gradientTicks[index*2+1])

        rbtn.setText('-')
        rbtn.setMaximumSize(QSize(20, 20))
        rbtn.clicked.connect(lambda: self._remove_color_range_slot(index))

        hlayout.setSpacing(10)
        hlayout.addWidget(drcw)
        hlayout.addWidget(rbtn)

        self.verticalLayout_2.addLayout(hlayout)

        return drcw

    def _add_plusBtn(self, index):
        abtn = QPushButton(self.scrollAreaWidgetContents)
        self._addButtons.append(abtn)
        abtn.setText('+')
        abtn.setMaximumSize(QSize(20, 20))
        abtn.clicked.connect(lambda: self._insert_color_range_slot(index))
        self.verticalLayout_2.addWidget(abtn, alignment=Qt.AlignHCenter)

    def _clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            cwidget = child.widget()
            if cwidget:
                cwidget.deleteLater()
            clayout = child.layout()
            if clayout:
                self._clearLayout(clayout)
                clayout.deleteLater()

    def applyGradientTicks(self, gradientTicks):
        self._rangeColorWidgets = []
        self._addButtons = []
        self._removeButtons = []

        self._clearLayout(self.verticalLayout_2)

        drcw = None
        drcw = self._add_drcWidget(0, gradientTicks, drcw)

        for i in xrange(1, len(gradientTicks)/2):
            self._add_plusBtn(i)
            drcw = self._add_drcWidget(i, gradientTicks, drcw)

        drcw.isLast = True

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

    def getGradientTicks(self):
        return list(chain.from_iterable(widget.getTuples() for widget in self._rangeColorWidgets))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = DiscreteColorRangeSelectorDialog()
    form.show()
    app.exec_()
