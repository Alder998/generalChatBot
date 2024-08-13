from Model import GPT2Model as bart

answer = bart.GPT2Model("How long is the Nile River?").generateAnswer()

print(answer)