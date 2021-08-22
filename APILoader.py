import urllib

import requests

from model.Country import Country
from model.DailyEntry import DailyEntry


class APILoader:
    data = []

    def load(self):
        """
        Ladet die Daten von der Github API herunter
        """
        # Downloaden der ~22 MB Datei
        link = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        f = urllib.request.urlopen(link)
        downloaded = f.read().decode('utf-8')
        # downloaded = downloaded.replace("\n", "¦")
        temp = str(downloaded).splitlines()
        firstrow = temp[0].split(",")
        maindata = temp[1:len(temp)]
        maindata.reverse()

        lastcountrycode = ""

        headers = {}

        for i in range(len(firstrow)):
            headers.update({firstrow[i]: int(i)})

        for i in maindata:
            rows = i.split(",")
            if lastcountrycode != rows[headers["iso_code"]]:
                lastcountrycode = rows[headers["iso_code"]]
                self.data.append(
                    Country(rows[headers["location"]], rows[headers["continent"]], rows[headers["iso_code"]]))
            country = self.data[len(self.data) - 1]
            result = {}
            for j in range(len(rows)):
                result.update({firstrow[j]: rows[j]})
            country.addEntry(DailyEntry(result))
        ignoreLocations = ["World", "Asia", "Africa", "Europe", "European Union", "North America", "South America", "Oceania", "International"]
        i = 0
        while i < len(self.data):
            if self.data[i].name in ignoreLocations or len(self.data[i].entries) < 100:
                self.data.pop(i)
            else:
                i += 1
        self.data.reverse()
        print(headers)