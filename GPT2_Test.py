from Model import GPT2Model as gpt2

prompt = "What is the city description of the City of Chiavari? please answer briefly"
answer = gpt2.GPT2Model(prompt).generateAnswer(model_name='./fine_tuned_gpt2')

print('\n')
print('Answer:', answer)