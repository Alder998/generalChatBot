from fineTuningDatasetGenerator import geographyDataset as geo
import pandas as pd

input_data = pd.read_excel(r"C:\Users\alder\Desktop\Projects\Fine Tuning Data\Europe_cities.xlsx")

geo.geographyScraper().downloadCitiesDescriptionBulkData(input_data, populationHigherThan=5000, populationLowerThan=0)
