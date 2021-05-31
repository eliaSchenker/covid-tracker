import urllib

import requests

from model.Country import Country
from model.DailyEntry import DailyEntry


class APILoader:
    data = []

    def load(self):
        # Downloaden der ~22 MB Datei
        link = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        f = urllib.request.urlopen(link)
        downloaded = f.read().decode('utf-8')
        # downloaded = downloaded.replace("\n", "¦")
        print(len(downloaded))
        temp = str(downloaded).splitlines()
        print(len(temp))
        firstrow = temp[0].split(",")
        maindata = temp[1:len(temp)]
        maindata.reverse()

        lastcountrycode = ""

        headers = {}

        for i in range(len(firstrow)):
            headers.update({firstrow[i]: int(i)})

        print(headers)

        for i in maindata:
            rows = i.split(",")
            if lastcountrycode != rows[headers["iso_code"]]:
                lastcountrycode = rows[headers["iso_code"]]
                self.data.append(
                    Country(rows[headers["location"]], rows[headers["continent"]], rows[headers["iso_code"]]))
            country = self.data[len(self.data) - 1]
            country.addEntry(DailyEntry(rows[headers["date"]],
                                        rows[headers["population"]],
                                        rows[headers["life_expectancy"]],
                                        rows[headers["new_cases"]],
                                        rows[headers["new_deaths"]],
                                        rows[headers["new_vaccinations"]],
                                        rows[headers["new_cases_per_million"]],
                                        rows[headers["new_deaths_per_million"]],
                                        rows[headers["total_cases"]],
                                        rows[headers["total_deaths"]],
                                        rows[headers["total_vaccinations"]]))
        self.data.reverse()
        print(self.data[0].name)
        print(self.data[0].entries[0].new_cases)
