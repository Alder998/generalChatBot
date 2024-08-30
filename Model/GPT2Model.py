# Small experiment to create a BART-based ChatBot

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import load_dataset
from fineTuningDatasetGenerator import fineTuning_Utils as utils

class GPT2Model:
    def __init__(self, prompt):
        self.inputText = prompt
        pass

    def generateAnswer (self, model_name='gpt2'):

        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)

        inputs = tokenizer(self.inputText, return_tensors='pt')

        attention_mask = inputs["attention_mask"]

        # Logging
        print('generating...')

        outputs = model.generate(inputs['input_ids'],
                                 num_return_sequences=1,
                                 num_beams=2,
                                 do_sample=True,
                                 attention_mask=attention_mask,
                                 temperature=0.5,
                                 top_k=30,
                                 top_p=0.9,
                                 #max_length=200,
                                 max_new_tokens=1000,
                                 eos_token_id=tokenizer.eos_token_id,
                                 pad_token_id=tokenizer.eos_token_id,
                                 repetition_penalty=2.0,
                                 no_repeat_ngram_size=5,
                                 early_stopping=True
                                 )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_text[len(self.inputText):len(generated_text)]


