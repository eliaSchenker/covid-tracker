import os
import sys
import time
import types
from datetime import datetime
from random import randint

import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *


class WorldMap(QMainWindow):
    def __init__(self, *args, **kwargs):

        super(WorldMap, self).__init__(*args, **kwargs)
        self.webEngineView = QWebEngineView()
        self.webEngineView.setStyleSheet("border: 5px solid #999999;")
        mainWidget = QWidget()
        self.setWindowTitle("World Map")
        self.setWindowIcon(QIcon(self.resource_path('icon.ico')))
        self.dropdownValues = ["new_cases", "new_cases_per_million", "total_cases", "new_deaths",
                               "new_deaths_per_million", "total_deaths", "new_vaccinations", "total_vaccinations"]

        self.displayBox = QComboBox()
        self.displayBox.addItem("Neue Infektionen")
        self.displayBox.addItem("Neue Infektionen pro Million")
        self.displayBox.addItem("Totale Infektionen")
        self.displayBox.addItem("Neue Tode")
        self.displayBox.addItem("Neue Tode pro Million")
        self.displayBox.addItem("Totale Tode")
        self.displayBox.addItem("Neue Impfungen")
        self.displayBox.addItem("Totale Impfungen")
        self.displayBox.currentIndexChanged.connect(self.loadWebView)

        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setStyleSheet("QSlider::groove:horizontal { " +
                              "border: 1px solid #999999; " +
                              "height: 20px; " +
                              "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4); " +
                              "margin: 2px 0; " +
                              "} " +
                              "QSlider::handle:horizontal { " +
                              "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f); " +
                              "border: 1px solid #5c5c5c; " +
                              "width: 30px; " +
                              "margin: -2px 0px; " +
                              "} ")
        self.timeSliderMinText = QLabel()
        self.timeSliderMinText.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.timeSliderMaxText = QLabel()
        self.timeSliderMaxText.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.timeSliderTextWidget = QWidget()
        self.timeSlider.sliderReleased.connect(self.loadWebView)
        self.timeSlider.valueChanged.connect(self.updateTitleText)

        self.timeSliderMinText.setMaximumHeight(30)
        self.timeSliderMaxText.setMaximumHeight(30)
        self.timeSliderTextWidget.setMaximumHeight(30)


        timeSliderTextWidgetLayout = QGridLayout()
        timeSliderTextWidgetLayout.addWidget(self.timeSliderMinText, 0, 0)
        timeSliderTextWidgetLayout.addWidget(self.timeSliderMaxText, 0, 1)

        self.timeSliderTextWidget.setLayout(timeSliderTextWidgetLayout)
        self.title = QLabel("Title")
        self.title.setMaximumHeight(60)
        self.title.setStyleSheet("font-size:25pt;font-weight:bold;")
        mainWidgetLayout = QVBoxLayout()
        mainWidget.setLayout(mainWidgetLayout)
        mainWidgetLayout.addWidget(self.title)
        mainWidgetLayout.addWidget(self.displayBox)
        mainWidgetLayout.addWidget(self.webEngineView)
        mainWidgetLayout.addWidget(self.timeSlider)
        mainWidgetLayout.addWidget(self.timeSliderTextWidget)
        self.setCentralWidget(mainWidget)

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    def loadWebView(self):
        with open(self.resource_path('WorldMapTemplate.html'), 'r') as f:
            html = f.read()
        colorValues = ""
        dataValues = ""
        minColor = QColor(173, 173, 173)
        maxColor = QColor(117, 0, 0)
        min = sys.maxsize
        max = 0

        usedKey = self.dropdownValues[self.displayBox.currentIndex()]

        for i in range(len(self.data)):
            entry = self.entryFromDate(i)
            if entry is not None:
                if entry.entry[usedKey] != '' and float(entry.entry[usedKey]) >= 0:
                    if float(entry.entry[usedKey]) > max:
                        max = float(entry.entry[usedKey])
                    if float(entry.entry[usedKey]) < min:
                        min = float(entry.entry[usedKey])

        for i in range(len(self.data)):
            entry = self.entryFromDate(i)
            if entry is not None:
                color = minColor
                if entry.entry[usedKey] != '' and float(entry.entry[usedKey]) >= 0:
                    t = (((float(entry.entry[usedKey]) - min) * (1 - 0)) / (max - min))
                    color = self.interpolateColors(minColor, maxColor, t)
                colorValues += "\"" + str(self.data[i].name) + "\" : \"" + str(color.name()) + "\","
                dataValues += "\"" + str(self.data[i].name) + "\" : \"\\n" + entry.entry[usedKey] + "\","

        colorValues = colorValues[0:len(colorValues) - 1]
        dataValues = dataValues[0:len(dataValues) - 1]
        html = html.replace("COLORVALUES", colorValues)
        html = html.replace("DATAVALUES", dataValues)
        html = html.replace("MINCOLOR", minColor.name())
        html = html.replace("MAXCOLOR", maxColor.name())
        html = html.replace("MINVALUE", str(min))
        html = html.replace("MAXVALUE", str(max))

        self.webEngineView.setHtml(html)

    def entryFromDate(self, countryIndex):
        entries = self.data[countryIndex].entries
        for i in entries:
            date = datetime.fromtimestamp(self.timeSlider.value())
            date = date.replace(hour=0, minute=0, second=0)
            if datetime.strptime(i.entry["date"], "%Y-%m-%d") == date:
                return i


    def getMinimumDate(self):
        minDate = sys.maxsize
        for i in self.data:
            date = datetime.timestamp(datetime.strptime(i.entries[-1].entry["date"], "%Y-%m-%d"))
            if date < minDate and date != 0:
                minDate = date
        return minDate

    def getMaximumDate(self):
        maxDate = 0
        for i in self.data:
            date = datetime.timestamp(datetime.strptime(i.entries[0].entry["date"], "%Y-%m-%d"))
            if date > maxDate and date != 0:
                maxDate = date
        return maxDate

    def setMinMaxSliderTexts(self):
        self.timeSlider.setTickInterval(86400)  # Jump forward in the timeline by one day
        self.timeSlider.setSingleStep(86400) #Jump forward in the timeline by one day
        self.timeSlider.setMinimum(self.getMinimumDate())
        self.timeSlider.setMaximum(self.getMaximumDate())

        self.timeSliderMinText.setText(datetime.strftime(datetime.fromtimestamp(self.timeSlider.minimum()), "%d-%m-%Y"))
        self.timeSliderMaxText.setText(datetime.strftime(datetime.fromtimestamp(self.timeSlider.maximum()), "%d-%m-%Y"))

        print(datetime.fromtimestamp(self.timeSlider.minimum()))
        print(datetime.fromtimestamp(self.timeSlider.maximum()))
        print((self.timeSlider.maximum() - self.timeSlider.minimum()) / 86400)

        self.timeSlider.setValue(self.timeSlider.maximum())
    def updateTitleText(self):
        self.title.setText("Weltkarte vom " + str(datetime.strftime(datetime.fromtimestamp(self.timeSlider.value()),
                                                                    "%d-%m-%Y")))
    def interpolateColors(self, a, b, t):
        return QColor(a.red() + (b.red() - a.red()) * t,
        a.green() + (b.green() - a.green()) * t,
        a.blue() + (b.blue() - a.blue()) * t,
        a.alpha() + (b.alpha()  - a.alpha() ) * t)
