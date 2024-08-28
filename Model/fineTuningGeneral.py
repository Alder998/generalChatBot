# File to handle Every Model's fine tuning

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import load_dataset
from fineTuningDatasetGenerator import fineTuning_Utils as utils
from transformers import Trainer, TrainingArguments

class fineTuningGeneral:

    def __init__(self):
        pass

    def fineTuningModel (self, baseModel, datasetPandas):
        # Load the Model and the Tokenizer that are needed to be trained
        tokenizer = GPT2Tokenizer.from_pretrained(baseModel)
        model = GPT2LMHeadModel.from_pretrained(baseModel)

        # Prepare the data that you want your Model to be trained on
        preparedText = utils.fineTuning_utils().getFineTuningContinuousTextFromDataset(datasetPandas)

        # Tokeinze the dataset
        inputs = tokenizer(preparedText, return_tensors='pt', max_length=1024, truncation=True)

        # Model fine-Tuning
        training_args = TrainingArguments(
            output_dir='./results',
            overwrite_output_dir=True,
            num_train_epochs=10,
            per_device_train_batch_size=1,
            save_steps=500,
            save_total_limit=2,
            logging_dir='./logs',
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=inputs,
        )
        trainer.train()

        model.save_pretrained('./fine_tuned_gpt2')
        tokenizer.save_pretrained('./fine_tuned_gpt2')

        return preparedText