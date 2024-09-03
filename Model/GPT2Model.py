# Small experiment to create a BART-based ChatBot

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import load_dataset
from fineTuningDatasetGenerator import fineTuning_Utils as utils
import tkinter as tk

class GPT2Model:
    def __init__(self, model_name):
        self.model_name = model_name
        pass

    def generateAnswer (self, prompt):

        tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        model = GPT2LMHeadModel.from_pretrained(self.model_name)

        inputs = tokenizer(prompt, return_tensors='pt')

        attention_mask = inputs["attention_mask"]

        # Logging
        print('generating...')

        outputs = model.generate(inputs['input_ids'],
                                 num_return_sequences=1,
                                 num_beams=2,
                                 do_sample=True,
                                 attention_mask=attention_mask,
                                 temperature=1.5,
                                 top_k=30,
                                 top_p=0.9,
                                 #max_length=200,
                                 max_new_tokens=100,
                                 eos_token_id=tokenizer.eos_token_id,
                                 pad_token_id=tokenizer.eos_token_id,
                                 #repetition_penalty=2.0,
                                 #no_repeat_ngram_size=5,
                                 early_stopping=True
                                 )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Post-processing to get concise Answers
        #generated_text = generated_text.split('.')[0:2] + '.'

        print('Answer generated correctly!')

        # Truncate the answers to avoid the question repetition
        return generated_text[len(prompt):len(generated_text)]

    # Try to put it into a Question/Answer setting
    def displayAnswer (self):

        # GUI
        root = tk.Tk()
        root.title("Chatbot")

        BG_GRAY = "#ABB2B9"
        BG_COLOR = "#17202A"
        TEXT_COLOR = "#EAECEE"

        FONT = "Helvetica 14"
        FONT_BOLD = "Helvetica 13 bold"

        # Send function
        def send():
            send = "You -> " + e.get()
            txt.insert(tk.END, "\n" + send)

            user = e.get().lower()

            if (user):
                txt.insert(tk.END, "\n" + "Bot -> " + self.generateAnswer(user))
                txt.insert(tk.END, "\n")

            e.delete(0, tk.END)

        lable1 = tk.Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text=self.model_name, font=FONT_BOLD, pady=10, width=20,
                       height=1).grid(
            row=0)

        txt = tk.Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
        txt.grid(row=1, column=0, columnspan=2)

        scrollbar = tk.Scrollbar(txt)
        scrollbar.place(relheight=1, relx=0.974)

        e = tk.Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
        e.grid(row=2, column=0)

        send = tk.Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                      command=send).grid(row=2, column=1)

        root.mainloop()




