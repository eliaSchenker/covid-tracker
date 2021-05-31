class DailyEntry():

    def __init__(self, date, population, life_expectency,
                 new_cases, new_deaths, new_vaccinations,
                 new_cases_per_million, new_deaths_per_million,
                 total_cases, total_deaths, total_vaccinations,
                 ):
        self.date = date
        self.population = population
        self.life_expectancy = life_expectency
        self.new_cases = new_cases
        self.new_deaths = new_deaths
        self.new_vaccinations = new_vaccinations
        self.new_cases_per_million = new_cases_per_million
        self.new_deaths_per_million = new_deaths_per_million
        self.total_cases = total_cases
        self.total_deaths = total_deaths
        self.total_vaccinations = total_vaccinations
