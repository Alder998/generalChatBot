from Model import GPT2Model as gpt2

prompt = "What is the DESCRIPTION of the CITY of Rome?"
model_name='./fine_tuned_gpt2_medium'
answer = gpt2.GPT2Model(model_name).generateAnswer(prompt)

print('\n')
print('Answer:', answer)