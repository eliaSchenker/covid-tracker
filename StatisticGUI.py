from random import randint

import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui


class StatisticGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(StatisticGUI, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setMenuEnabled(False)
        self.graphWidget.setBackground('w')
        self.graphWidget.addLegend()

        self.countrySelection = QListWidget()
        self.countrySelection.itemSelectionChanged.connect(self.updateGraph)
        self.countrySelection.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.sortBox = QComboBox()
        self.sortBox.addItem("Name")
        self.sortBox.addItem("Infektionen Gesamt")

        self.displayBox = QComboBox()
        self.displayBox.addItem("Neue Infektionen")
        self.displayBox.addItem("Neue Infektionen pro Million")
        self.displayBox.addItem("Neue Tode")
        self.displayBox.addItem("Neue Tode pro Million")

        self.displayBox.currentIndexChanged.connect(self.updateGraph)

        selectAllButton = QPushButton("Alles selektieren")
        deselectAllButton = QPushButton("Nichts selektieren")

        selectAllButton.clicked.connect(self.countrySelection.selectAll)
        deselectAllButton.clicked.connect(self.countrySelection.clearSelection)

        mainWidget = QWidget()
        controlWidget = QWidget()

        layout = QGridLayout()
        controlWidgetLayout = QVBoxLayout()

        controlWidgetLayout.addWidget(QLabel("Sortieren nach:"))
        controlWidgetLayout.addWidget(self.sortBox)
        controlWidgetLayout.addWidget(QLabel("Angezeigte Daten:"))
        controlWidgetLayout.addWidget(self.displayBox)
        controlWidgetLayout.addWidget(self.countrySelection)
        controlWidgetLayout.addWidget(selectAllButton)
        controlWidgetLayout.addWidget(deselectAllButton)

        controlWidget.setLayout(controlWidgetLayout)

        layout.addWidget(self.graphWidget, 0, 0)
        layout.addWidget(controlWidget, 0, 1)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def setStats(self, data):
        self.data = data
        self.countrySelection.clear()
        for i in data:
            self.countrySelection.addItem(i.name)

    def updateGraph(self):
        self.graphWidget.clear()
        selectedIndexes = []

        dropdownValues = ["new_cases", "new_cases_per_million", "new_deaths", "new_deaths_per_million"]

        for i in self.countrySelection.selectedIndexes():
            selectedIndexes.append(i.row())
        for i in range(len(self.data)):
            if i in selectedIndexes:
                tempInfections = []
                tempDates = []
                count = 0
                for j in self.data[i].entries:
                    entryValue = j.entry[dropdownValues[self.displayBox.currentIndex()]]
                    if entryValue != '' and entryValue != 0:
                        tempInfections.append(float(entryValue))
                        tempDates.append(count)
                    count += 1
                self.drawStats(tempDates, tempInfections, self.data[i].name)

    def drawStats(self, dates, infections, countryname):
        self.graphWidget.plot(dates, infections, pen=pg.mkPen(color=(randint(0, 255), randint(0, 255), randint(0, 255)), width=1), name=countryname)

