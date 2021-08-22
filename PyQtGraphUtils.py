from datetime import datetime
import pyqtgraph as pg

#Zusatzklasse für den PyqtGraph (zeigt anstatt ein Timestamp ein Datum in der Zeitachse an.
class TimeAxisItem(pg.AxisItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%d.%m.%Y") for value in values]
