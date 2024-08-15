# The aim is to create a conversation DB to train a chatBot to answer basic questions

import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

# Example Dataset
cities = pd.read_excel(r"C:\Users\alder\Desktop\Projects\Fine Tuning Data\Cities Italy.xlsx")

# Filter the data (if necessary)
cities = cities[(cities['population'] < 11000) & (cities['population'] > 10000)]

citiesDatabase = list()
for index, city in enumerate(list(cities['city'])):

    print('Processing City/Town:', city, ' - Progress:', round((index / len(cities['city'])) * 100, 2), '%')

    # Adapt the city name
    if len(city) > 1:
        city = city.replace(' ', '_')

    target_url = "https://en.wikipedia.org/wiki/" + city

    resp = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')  # Pare che l'URL sia libero per fare scraping

    content_div = soup.find('div', class_='mw-content-ltr mw-parser-output', href=False)

    try:
        # Find paragraph <p> in the div
        allParagraph = content_div.find_all('p')

        paragraphData = []
        for paragraph in allParagraph:
            if paragraph.text:
                paragraphData.append(paragraph.text)
        paragraphData = " ".join(paragraphData)
        paragraphData = paragraphData.replace('\n', '')

        # Format to save to SQL
        cityData = pd.DataFrame(pd.Series(city)).set_axis(['City'], axis=1)
        paragraphData = pd.DataFrame(pd.Series(paragraphData)).set_axis(['City Description'], axis=1)
        finalPayload = pd.concat([cityData, paragraphData], axis=1)
        citiesDatabase.append(finalPayload)

    except Exception as e:
        print('No Wikipedia Data on the city:', city)


citiesDatabase = pd.concat([series for series in citiesDatabase], axis=0).reset_index(drop=True)

# Load the existing Data
engine = create_engine('postgresql://postgres:Lavagna123!@localhost:5432/fineTuningData')
query = 'SELECT * FROM public."ItalianCitiesData"'
baseData = pd.read_sql(query, engine)

# Append The new data to the old ones, drop duplicates
finalDataset = pd.concat([baseData, citiesDatabase], axis=0).drop_duplicates(keep='last').reset_index(drop=True)

# Save the data in the database
file = finalDataset
connection = psycopg2.connect(
    database="fineTuningData",
    user="postgres",
    password="Lavagna123!",
    host="localhost",
    port="5432"
)
engine = create_engine('postgresql://postgres:Lavagna123!@localhost:5432/fineTuningData')
file.to_sql('ItalianCitiesData', engine, if_exists='replace', index=False)

# Close the connection to the DB
connection.close()

# Print the final Data
print(finalDataset)
