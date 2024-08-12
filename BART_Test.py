from Model import BARTModel as bart

answer = bart.BARTModel("Ciao, come stai oggi?").generateAnswer()

print(answer)