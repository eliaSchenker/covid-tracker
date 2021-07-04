from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from APILoader import APILoader
from StatisticGUI import StatisticGUI
from WorldMap import WorldMap


class MenuGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MenuGUI, self).__init__(*args, **kwargs)

        mainWidget = QWidget()

        layout = QVBoxLayout()

        loader = APILoader()
        loader.load()

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Covid Tracker")
        self.main = StatisticGUI()
        self.main.setStats(loader.data)
        self.main.updateGraph()

        self.worldmap = WorldMap()
        self.worldmap.data = loader.data
        self.worldmap.setMinMaxSliderTexts()
        self.worldmap.loadWebView()

        title = QLabel("Covid Tracker")
        worldmapbutton = QPushButton("Weltkarte")
        worldmapbutton.clicked.connect(self.showWorldMap)
        statisticButton = QPushButton("Statistik")
        statisticButton.clicked.connect(self.showStatistic)
        title.setStyleSheet("font-size:25pt;font-weight:bold;")

        layout.addWidget(title)
        layout.addWidget(statisticButton)
        layout.addWidget(worldmapbutton)

        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
    def showStatistic(self):
        self.main.showMaximized()
    def showWorldMap(self):
        self.worldmap.showMaximized()

