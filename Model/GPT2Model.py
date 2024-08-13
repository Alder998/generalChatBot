# Small experiment to create a BART-based ChatBot

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

class GPT2Model:
    def __init__(self, inputText):
        self.inputText = inputText
        pass

    def generateAnswer (self):

        model_name = 'gpt2'
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)

        inputs = tokenizer(self.inputText, return_tensors='pt', max_length=1024, truncation=True)

        attention_mask = inputs["attention_mask"]

        outputs = model.generate(inputs['input_ids'], num_return_sequences=1, attention_mask=attention_mask, max_new_tokens=50,
                                 eos_token_id=tokenizer.eos_token_id)

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_text