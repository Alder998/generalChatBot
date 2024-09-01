from fineTuningDatasetGenerator import geographyDataset as geo
import pandas as pd

input_data = pd.read_excel(r"C:\Users\alder\Desktop\Projects\Fine Tuning Data\World Cities_short.xlsx")

# Filter for Europe
input_data = input_data[(input_data['country'] == 'Serbia') | (input_data['country'] == 'Bosnia and Herzegovina') | (input_data['country'] == 'Belgium')
                        | (input_data['country'] == 'Netherlands') | (input_data['country'] == 'Luxembourg')]

#geo.geographyScraper().(input_data, populationHigherThan=10000, populationLowerThan=0)

geo.geographyScraper().integrateDBWithCoordinates()