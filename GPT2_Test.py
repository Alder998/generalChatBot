from Model import GPT2Model as gpt2

answer = gpt2.GPT2Model("What can you tell me about the city of Lavagna?").generateAnswer()

print(answer)