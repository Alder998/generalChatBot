from Model import GPT2Model as gpt2

answer = gpt2.GPT2Model("What is your name? Please give me a short answer").generateAnswer()

print(answer)