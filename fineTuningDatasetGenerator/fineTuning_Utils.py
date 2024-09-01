# General file for multi-usage functions for processing text data for fine-tuning

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

class fineTuning_utils:

    def __init__(self):
        pass

    def getFineTuningContinuousTextFromDataset (self, datasetPandas):

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
            totalStringList.append('\n' + '\n')
        totalStringList = ' '.join(totalStringList)

        return totalStringList

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
