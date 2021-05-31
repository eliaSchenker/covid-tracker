class Country:

    def __init__(self, name, continent, code):
        self.name = name
        self.continent = continent
        self.code = code
        self.entries = []

    def addEntry(self, entry):
        self.entries.append(entry)

    def removeEntry(self, index):
        self.entries.remove(index)
