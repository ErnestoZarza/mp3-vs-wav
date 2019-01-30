import sys

from PyQt4.QtCore import QSize
from PyQt4.QtGui import QDialog, QPushButton, QSizePolicy, QApplication, QHBoxLayout, QSpacerItem, \
    QLabel, QLinearGradient, QColor, QBrush, QPalette

from colorScaleStuff.GradientColorWidget import GradientColorWidget
from colorScaleStuff.ui_discreteColorRangeSelectorDialog import Ui_discreteColorRangeSelector
from widgets import utils


class GradientColorSelectorDialog(QDialog, Ui_discreteColorRangeSelector):  # not an error; it actually uses the same ui
    def __init__(self, parent=None, gradientTicks=None):
        if parent is not None:
            super(GradientColorSelectorDialog, self).__init__(parent)
        else:
            super(GradientColorSelectorDialog, self).__init__()

        self.setupUi(self)

        self.utils = utils.utils()

        if gradientTicks is None:
            gradientTicks = self.utils.defaultContinuousColorGradientTicks

        self._rangeColorWidgets = []
        self._addButtons = []
        self._removeButtons = []
        self.applyGradientTicks(gradientTicks)

    def _insert_color_range_slot(self, index):
        gradientTicks = self.getGradientTicks()

        if not (0 < index < len(gradientTicks)):
            return

        pos = (gradientTicks[index-1][0] + gradientTicks[index][0]) / 2.
        color_prev = gradientTicks[index-1][1]
        color_next = gradientTicks[index][1]
        color = tuple((x1+x2)/2 for x1, x2 in zip(color_prev, color_next))

        gradientTicks.insert(index, (pos, color))

        self.applyGradientTicks(gradientTicks)

    def _remove_color_range_slot(self, index):
        gradientTicks = self.getGradientTicks()

        if len(gradientTicks) <= 2 or not (0 <= index < len(gradientTicks)):
            return

        del gradientTicks[index]

        if index == 0:
            gradientTicks[0] = 0, gradientTicks[0][1]
        elif index == len(gradientTicks) - 1:
            gradientTicks[-1] = 1, gradientTicks[-1][1]

        self.applyGradientTicks(gradientTicks)

    def _add_drcWidget(self, index, gradientTicks):
        drcw = GradientColorWidget(self.scrollAreaWidgetContents)
        rbtn = QPushButton(self.scrollAreaWidgetContents)
        hlayout = QHBoxLayout()

        self._rangeColorWidgets.append(drcw)
        self._removeButtons.append(rbtn)

        drcw.applyTuple(gradientTicks[index])
        drcw.colorChanged.connect(lambda: self.applyGradientTicks(self.getGradientTicks()))

        rbtn.setText('-')
        rbtn.setMaximumSize(QSize(20, 20))
        rbtn.clicked.connect(lambda: self._remove_color_range_slot(index))

        hlayout.setSpacing(10)
        hlayout.addWidget(drcw)
        hlayout.addWidget(rbtn)

        self.verticalLayout_2.addLayout(hlayout)

        return drcw

    def _add_plusBtn(self, index, gradientTicks):
        abtn = QPushButton(self.scrollAreaWidgetContents)
        rlabel = QLabel(self.scrollAreaWidgetContents)
        hlayout = QHBoxLayout()

        self._addButtons.append(abtn)
        abtn.setText('+')
        abtn.setMaximumSize(QSize(20, 20))
        abtn.clicked.connect(lambda: self._insert_color_range_slot(index))

        gradient = QLinearGradient(0, 0, 0, 20)
        gradient.setColorAt(0, QColor(*gradientTicks[index-1][1]))
        gradient.setColorAt(1, QColor(*gradientTicks[index][1]))
        brush = QBrush(gradient)

        rlabel.setAutoFillBackground(True)
        palette = rlabel.palette()
        palette.setBrush(QPalette.Window, brush)
        rlabel.setPalette(palette)
        rlabel.setMaximumSize(QSize(20, 20))
        rlabel.setMinimumSize(QSize(20, 20))

        # hlayout.setSpacing(5)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hlayout.addItem(spacer)
        hlayout.addWidget(abtn)
        hlayout.addWidget(rlabel)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hlayout.addItem(spacer)
        # hlayout.setStretch(0, 40)
        # hlayout.setStretch(1, 10)
        # hlayout.setStretch(2, 30)
        # hlayout.setStretch(3, 10)

        self.verticalLayout_2.addLayout(hlayout)

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

        drcw = self._add_drcWidget(0, gradientTicks)
        drcw.isFirst = True

        for i in xrange(1, len(gradientTicks)):
            self._add_plusBtn(i, gradientTicks)
            drcw = self._add_drcWidget(i, gradientTicks)

        drcw.isLast = True

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

    def getGradientTicks(self):
        return [widget.getTuple() for widget in self._rangeColorWidgets]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = GradientColorSelectorDialog()
    form.show()
    app.exec_()
