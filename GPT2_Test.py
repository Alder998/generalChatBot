from Model import GPT2Model as gpt2

answer = gpt2.GPT2Model("What are the main Financial News of Yesterday?").generateAnswer()

print(answer)