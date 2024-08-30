from Model import GPT2Model as gpt2

# Application general Test

model_name='./fine_tuned_gpt2_medium'
answer = gpt2.GPT2Model(model_name).displayAnswer()

