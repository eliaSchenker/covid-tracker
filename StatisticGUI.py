from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtNetwork
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import pyqtgraph as pg


class StatisticGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(StatisticGUI, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setMenuEnabled(False)
        self.graphWidget.setBackground('w')
        self.setCentralWidget(self.graphWidget)

    def drawStats(self, dates, infections, label):
        self.graphWidget.setTitle(label)
        for i in range(len(infections)):
            self.graphWidget.plot(dates[i], infections[i], pen=pg.mkPen(color=(0, 0, 0), width=1))
