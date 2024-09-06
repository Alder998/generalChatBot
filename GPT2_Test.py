from Model import GPT2Model as gpt2

prompt = "Can you tell me the news of the ticker AMZN of Today"
model_name='./fine_tuned_gpt2_medium'
answer = gpt2.GPT2Model(model_name).generateAnswer(prompt)

print('\n')
print('Answer:', answer)