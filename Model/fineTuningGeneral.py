# File to handle Every Model's fine tuning

import torch
from torch.utils.data import DataLoader
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import load_dataset
from fineTuningDatasetGenerator import fineTuning_Utils as utils
from transformers import Trainer, TrainingArguments

class fineTuningGeneral:

    def __init__(self):
        pass

    def fineTuningModel (self, baseModel, datasetPandas, epochs, saved_model_name='fine_tuned_gpt2'):
        # Load the Model and the Tokenizer that are needed to be trained
        tokenizer = GPT2Tokenizer.from_pretrained(baseModel)
        model = GPT2LMHeadModel.from_pretrained(baseModel)

        # Add special Tokens (dataset columns)
        special_tokens_dict = {
            'additional_special_tokens': utils.fineTuning_utils().getFineTuningContinuousTextFromDataset(datasetPandas, return_special_tokens=True)}
        tokenizer.add_special_tokens(special_tokens_dict)
        model.resize_token_embeddings(len(tokenizer))

        # Prepare the data that you want your Model to be trained on
        preparedText = utils.fineTuning_utils().getFineTuningContinuousTextFromDataset(datasetPandas)

        # Tokeinze the dataset
        inputs = tokenizer(preparedText, return_tensors='pt', max_length=1024, truncation=True)
        inputs['labels'] = inputs['input_ids'].clone()

        # Divide in Batch
        dataset = utils.TextDataset(inputs)
        dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

        # Model fine-Tuning
        training_args = TrainingArguments(
            output_dir='./results',
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=1,
            save_steps=500,
            save_total_limit=2,
            logging_dir='./logs',
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
        )
        trainer.train()

        model.save_pretrained('./' + saved_model_name)
        tokenizer.save_pretrained('./' + saved_model_name)

        print('Model and Tokenizer saved correctly! Find them at ' + saved_model_name)

        return preparedText