# General file for multi-usage functions for processing text data for fine-tuning
from datetime import datetime

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
import psycopg2
import numpy as np
from sqlalchemy import create_engine

class fineTuning_utils:

    def __init__(self):
        pass

    def getFineTuningContinuousTextFromDataset (self, datasetPandas, return_special_tokens=False):

        # Prepare the dataset in JSON format, before converting it into continuous text
        dictList = list()
        for singleRow in range(len(datasetPandas[datasetPandas.columns[0]])):
            singleRowData = pd.DataFrame(datasetPandas.iloc[singleRow]).transpose().reset_index(drop=True)
            dictList.append(singleRowData.iloc[0].to_dict())

        # Then, the file needs to be converted into Continuous Text format, with delimiters to help the model understand
        # what is the topic of the fine-tuning Dataset, therefore, the settings must be <COLUMN_NAME> text </COLUMN_NAME>
        # and so on. The desired file has to be a long string file with all the fine-tuning information

        totalStringList = list()
        for singleDict in dictList:
            for key, value in singleDict.items():
                # Compose the long Text for any single Item
                continuousTextSingleString = ('<' + key.upper() + '> ' + str(value) + ' </' + key.upper() + '> ' + '\n')
                totalStringList.append(continuousTextSingleString)

            if return_special_tokens:
                specialTokens = []
                for key, value in singleDict.items():
                    special_token_start = ('<' + key.upper() + '>')
                    special_token_end = ('</' + key.upper() + '>')
                    specialTokens.append(special_token_start)
                    specialTokens.append(special_token_end)

                print(specialTokens)
                return specialTokens

            totalStringList.append('\n' + '\n')
        totalStringList = ' '.join(totalStringList)

        # Save the Total StringList to a .txt file, so we can check it while the model is training
        with open(r'C:\Users\alder\Desktop\Projects\Fine Tuning Data\fineTuning_str.txt', 'w') as file:
            try:
                file.write(totalStringList)
            except Exception as e:
                print('Unable to save')

        print(totalStringList)

        return totalStringList

    def loadAndProcessFinancialNews (self, newsDataset):

        # it is taken a DataFrame
        newsDataset['Day'] = (datetime.today() - pd.to_datetime(newsDataset['Date'])).dt.days
        newsDataset['Day'] = newsDataset['Day'].astype(str) + ' days ago'
        newsDataset.loc[newsDataset['Day'] == '0 days ago', 'Day'] = 'Today'
        newsDataset.loc[newsDataset['Day'] == '1 days ago', 'Day'] = 'Yesterday'

        file = newsDataset
        connection = psycopg2.connect(
            database="YahooFinance",
            user="postgres",
            password="Lavagna123!",
            host="localhost",
            port="5432"
        )
        engine = create_engine('postgresql://postgres:Lavagna123!@localhost:5432/YahooFinance')
        file.to_sql('News_Scraping_Data_V3_chatbot', engine, if_exists='replace', index=False)
        connection.close()

        return newsDataset

# Text loader

class TextDataset(Dataset):
    def __init__(self, encodings):
        self.input_ids = encodings.input_ids
        self.attention_mask = encodings.attention_mask

        # Imposta i labels come input_ids
        self.labels = encodings.input_ids.clone()

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.labels[idx]
        }

    def __len__(self):
        return len(self.input_ids)
