from fineTuningDatasetGenerator import geographyDataset as geo
import pandas as pd

input_data = pd.read_excel(r"C:\Users\alder\Desktop\Projects\Fine Tuning Data\World Cities_short.xlsx")

# Filter for Europe
input_data = input_data[(input_data['country'] == 'Germany') | (input_data['country'] == 'France') | (input_data['country'] == 'Spain') |
                        (input_data['country'] == 'Portugal') | (input_data['country'] == 'Germany')]

geo.geographyScraper().downloadCitiesDescriptionBulkData(input_data, populationHigherThan=15000, populationLowerThan=30000)