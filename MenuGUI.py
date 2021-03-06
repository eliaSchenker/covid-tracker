import os
import sys

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

        # Hilfefenster anzeigen, welches das herunterladen der Daten anzeigt
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle("Bitte warten...")
        msg.setText("Neue Daten werden heruntergeladen. Bitte warten...")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


        loader = APILoader()
        loader.load()

        #Fenster schliessen, sobald das Laden beendet ist.
        msg.close()

        #Fenster-Icon und Titel setzen
        self.setWindowIcon(QIcon(self.resource_path('icon.ico')))
        self.setWindowTitle("Covid Tracker")

        #Daten setzen und Weltkarte vorbereiten
        self.main = StatisticGUI()
        self.main.setStats(loader.data)
        self.main.updateGraph()

        self.worldmap = WorldMap()
        self.worldmap.data = loader.data
        self.worldmap.setMinMaxSliderTexts()
        self.worldmap.loadWebView()

        #GUI des Menüs erstellen
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

    def resource_path(self, relative_path):
        """
        Funktion zum umwandeln der Pfade in der Resourcen (z.B Icon) zu Pfaden, welche von dem .exe export verwendet werden
        :param relative_path: Relativer Pfad (z.B icon.ico)
        :return: Neuer Pfad
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)
    def showStatistic(self):
        """
        Statistik anzeigen
        """
        self.main.showMaximized()
    def showWorldMap(self):
        """
        Weltkarte anzeigen
        """
        self.worldmap.showMaximized()

