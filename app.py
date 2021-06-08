# Main App Script
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

from APILoader import APILoader
from StatisticGUI import StatisticGUI

loader = APILoader()
loader.load()
dates = []
infections = []
count = 0

name = "World"
for i in loader.data:
    tempInfections = []
    tempDates = []
    count = 0
    for j in i.entries:
        if j.new_cases != '' and j.new_cases != 0:
            tempInfections.append(float(j.new_cases))
            tempDates.append(count)
            count += 1
    infections.append(tempInfections)
    dates.append(tempDates)
app = QtWidgets.QApplication(sys.argv)
main = StatisticGUI()
main.drawStats(dates, infections, name)
main.show()
sys.exit(app.exec_())
