from PyQt5.QtWidgets import *

from APILoader import APILoader
from StatisticGUI import StatisticGUI


class MenuGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MenuGUI, self).__init__(*args, **kwargs)

        mainWidget = QWidget()

        layout = QVBoxLayout()

        loader = APILoader()
        loader.load()

        self.main = StatisticGUI()
        self.main.setStats(loader.data)
        self.main.updateGraph()

        title = QLabel("Covid Tracker")
        statisticButton = QPushButton("Statistik")
        statisticButton.clicked.connect(self.showStatistic)
        title.setStyleSheet("font-size:100%")

        layout.addWidget(title)
        layout.addWidget(statisticButton)

        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
    def showStatistic(self):
        self.main.showMaximized()

