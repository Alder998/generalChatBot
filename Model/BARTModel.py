# Small experiment to create a BART-based ChatBot

import torch
from transformers import BartTokenizer, BartForConditionalGeneration

class BARTModel:
    def __init__(self, inputText):
        self.inputText = inputText
        pass

    def generateAnswer (self):

        model_name = 'facebook/bart-large'
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)

        inputs = tokenizer(self.inputText, return_tensors='pt', max_length=1024, truncation=True)

        outputs = model.generate(inputs['input_ids'], max_length=50, num_beams=5, temperature=0.7,
                                 top_k=50, top_p=0.95, early_stopping=True)

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_text