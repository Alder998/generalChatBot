# File to handle Every Model's fine tuning

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import load_dataset
from fineTuningDatasetGenerator import fineTuning_Utils as utils

class fineTuningGeneral:

    def __init__(self):
        pass

    def fineTuningModel (self, baseModel, datasetPandas):
        # Load the Model and the Tokenizer that are needed to be trained
        tokenizer = GPT2Tokenizer.from_pretrained(baseModel)
        model = GPT2LMHeadModel.from_pretrained(baseModel)

        # Prepare the data that you want your Model to be trained on

        preparedText = utils.fineTuning_utils().getFineTuningContinuousTextFromDataset(datasetPandas)

        return preparedText