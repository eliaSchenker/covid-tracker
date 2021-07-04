import os
import sys
import time
from datetime import datetime
from random import randint

import pyqtgraph as pg
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from pyqtgraph import LabelItem

from PyQtGraphUtils import TimeAxisItem


class StatisticGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(StatisticGUI, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget(
            title="Covid-19 Data",
            labels= {'left': "Neue Infektionen"},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )
        sshFile = self.resource_path('style.stylesheet')
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        self.setWindowIcon(QIcon(self.resource_path('icon.ico')))
        self.setWindowTitle("Statistic")
        self.graphWidget.setMenuEnabled(False)
        self.graphWidget.setBackground('w')
        self.graphWidget.addLegend()

        self.dropdownValues = ["new_cases", "new_cases_per_million", "total_cases", "new_deaths", "new_deaths_per_million", "total_deaths", "new_vaccinations", "total_vaccinations"]

        self.countrySelection = QListWidget()
        self.countrySelection.itemSelectionChanged.connect(self.updateGraph)
        self.countrySelection.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.sortBox = QComboBox()
        self.sortBox.addItem("Name")
        self.sortBox.addItem("Höchster Wert")

        self.displayBox = QComboBox()
        self.displayBox.addItem("Neue Infektionen")
        self.displayBox.addItem("Neue Infektionen pro Million")
        self.displayBox.addItem("Totale Infektionen")
        self.displayBox.addItem("Neue Tode")
        self.displayBox.addItem("Neue Tode pro Million")
        self.displayBox.addItem("Totale Tode")
        self.displayBox.addItem("Neue Impfungen")
        self.displayBox.addItem("Totale Impfungen")

        self.displayBox.currentIndexChanged.connect(self.updateGraph)

        selectAllButton = QPushButton("Alles selektieren")
        deselectAllButton = QPushButton("Nichts selektieren")
        exportDataButton = QPushButton("Daten exportieren")

        selectAllButton.clicked.connect(self.countrySelection.selectAll)
        deselectAllButton.clicked.connect(self.countrySelection.clearSelection)
        exportDataButton.clicked.connect(self.saveData)

        selectAllButton.setStyleSheet("border-radius:10px;background-color:gray")

        selectAllButton.setStyleSheet("")

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
        controlWidgetLayout.addWidget(exportDataButton)

        controlWidget.setLayout(controlWidgetLayout)

        layout.addWidget(self.graphWidget, 0, 0)
        layout.addWidget(controlWidget, 0, 1)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    def setStats(self, data):
        self.data = data
        self.countrySelection.clear()
        for i in data:
            self.countrySelection.addItem(i.name)

    def saveData(self):
        path = QFileDialog.getSaveFileName(self, 'Export Data', 'data.csv', '.csv')
        file = open(path[0], 'w')
        if path != ('', ''):
            selectedIndexes = self.getSelectedIndexes()
            export = ""
            exportheaders = ""
            headerkeys = list(self.data[0].entries[0].entry)
            for i in range(len(headerkeys)):
                if i == len(headerkeys) - 1:
                    exportheaders += headerkeys[i]
                else:
                    exportheaders += headerkeys[i] + ", "

            for i in range(len(self.data)):
                if i in selectedIndexes:
                    for j in self.data[i].entries:
                        entries = list(j.entry.values())
                        for k in range(len(entries)):
                            if k == len(entries) - 1:
                                export += entries[k] + "\n"
                            else:
                                export += entries[k] + ", "

            file.write(exportheaders + "\n" + export)
            file.close()

    def getSelectedIndexes(self):
        selectedIndexes = []
        for i in self.countrySelection.selectedIndexes():
            selectedIndexes.append(i.row())
        return selectedIndexes

    def updateGraph(self):
        self.graphWidget.clear()
        self.graphWidget.setLabel('left', self.displayBox.currentText())
        selectedIndexes = self.getSelectedIndexes()

        for i in range(len(self.data)):
            if i in selectedIndexes:
                tempData = []
                tempDates = []
                count = 0
                for j in self.data[i].entries:
                    entryValue = j.entry[self.dropdownValues[self.displayBox.currentIndex()]]

                    if entryValue != '' and entryValue != "0.0" and float(entryValue) > 0:
                        tempData.append(float(entryValue))
                        tempDates.append(int(time.mktime(
                            datetime.strptime(j.entry["date"] + " 00:00:00", "%Y-%m-%d %H:%M:%S").timetuple())))
                    count += 1
                self.drawStats(tempDates, tempData, self.data[i].name)
        self.graphWidget.autoRange()

    def drawStats(self, dates, infections, countryname):
        self.graphWidget.plot(dates, infections, pen=pg.mkPen(color=(randint(0, 200), randint(0, 200), randint(0, 200)),
                                                              width=1), name=countryname)
