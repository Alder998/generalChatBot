from Model import GPT2Model as gpt2

prompt = "Can you tell me the CITY DESCRIPTION of the CITY of Lavagna?"
model_name='./fine_tuned_gpt2_medium'
answer = gpt2.GPT2Model(model_name).generateAnswer(prompt)

print('\n')
print('Answer:', answer)