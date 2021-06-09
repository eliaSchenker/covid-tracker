# Main App Script
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

from APILoader import APILoader
from MenuGUI import MenuGUI
from StatisticGUI import StatisticGUI


app = QtWidgets.QApplication(sys.argv)

menuGUI = MenuGUI()
menuGUI.show()

sys.exit(app.exec_())
