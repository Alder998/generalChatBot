from Model import GPT2Model as gpt2

answer = gpt2.GPT2Model("What are the main financial News about the ticker NFLX?").generateAnswer(model_name='./fine_tuned_gpt2')

print(answer)