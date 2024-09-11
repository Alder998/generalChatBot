# The aim is to create a conversation DB to train a chatBot to answer basic questions

import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import math
from sqlalchemy import create_engine

class geographyScraper:
    def __init__(self):
        pass

    def downloadCitiesDescriptionBulkData (self, input_data, populationHigherThan=0, populationLowerThan=0):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

        # Example Dataset - must have a pre-determined shape and columns name
        cities = input_data

        # Filter the data (if necessary)
        if (populationLowerThan != 0) & (populationHigherThan != 0):
            cities = cities[(cities['population'] < populationLowerThan) & (cities['population'] > populationHigherThan)]
        elif populationHigherThan != 0:
            cities = cities[cities['population'] > populationHigherThan]
        elif populationLowerThan != 0:
            cities = cities[cities['population'] < populationLowerThan]

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

        # merge the additional Information
        allCitiesFile = pd.read_excel(r"C:\Users\alder\Desktop\Projects\Fine Tuning Data\Europe cities full.xlsx")
        finalDataset = finalDataset.merge(
            allCitiesFile[['city','lat','lng','country','admin_name','population']],
            left_on=['City'], right_on=['city'], how='left')

        # Avoid duplicated Columns
        if 'lat_x' in finalDataset.columns:
            finalDataset.loc[~finalDataset['lat_x'].isna() & finalDataset['lat_y'].isna(), 'lat'] = finalDataset['lat_x']
            finalDataset.loc[~finalDataset['lat_y'].isna() & finalDataset['lat_x'].isna(), 'lat'] = finalDataset['lat_y']
            del[finalDataset['lat_x']]
            del[finalDataset['lat_y']]

        if 'lng_x' in finalDataset.columns:
            finalDataset.loc[~finalDataset['lng_x'].isna() & finalDataset['lng_y'].isna(), 'lng'] = finalDataset['lng_x']
            finalDataset.loc[~finalDataset['lng_y'].isna() & finalDataset['lng_x'].isna(), 'lng'] = finalDataset['lng_y']
            del[finalDataset['lng_x']]
            del[finalDataset['lng_y']]

        if 'city_x' in finalDataset.columns:
            finalDataset.loc[~finalDataset['city_x'].isna() & finalDataset['city_y'].isna(), 'city'] = finalDataset['city_x']
            finalDataset.loc[~finalDataset['city_y'].isna() & finalDataset['city_x'].isna(), 'city'] = finalDataset['city_y']
            del[finalDataset['city_x']]
            del[finalDataset['city_y']]

        if 'country_x' in finalDataset.columns:
            finalDataset.loc[~finalDataset['country_x'].isna() & finalDataset['country_y'].isna(), 'country'] = finalDataset['country_x']
            finalDataset.loc[~finalDataset['country_y'].isna() & finalDataset['country_x'].isna(), 'country'] = finalDataset['country_y']
            del[finalDataset['country_y']]
            del[finalDataset['country_x']]

        if 'population_x' in finalDataset.columns:
            finalDataset.loc[~finalDataset['population_x'].isna() & finalDataset['population_y'].isna(), 'population'] = finalDataset['population_x']
            finalDataset.loc[~finalDataset['population_y'].isna() & finalDataset['population_x'].isna(), 'population'] = finalDataset['population_y']
            del[finalDataset['population_y']]
            del[finalDataset['population_x']]

        finalDataset['Population'] = finalDataset['population'].apply(lambda x: f"{x:,}")
        del [finalDataset['population']]
        finalDataset['Region'] = finalDataset['admin_name']
        del [finalDataset['admin_name']]

        finalDataset = finalDataset.drop_duplicates(subset = ['City', 'City Description'])

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

        return finalDataset
