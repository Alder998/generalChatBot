from Model import BARTModel as bart

answer = bart.BARTModel("Come stai?").generateAnswer()

print(answer)