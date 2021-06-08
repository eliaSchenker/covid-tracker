# Main App Script
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

from APILoader import APILoader
from StatisticGUI import StatisticGUI

loader = APILoader()
loader.load()

app = QtWidgets.QApplication(sys.argv)

main = StatisticGUI()
main.setStats(loader.data)
main.updateGraph()

main.show()
sys.exit(app.exec_())
