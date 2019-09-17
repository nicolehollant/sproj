from RandomReplacement.model import Model
import re

model = Model()
# model.entryExists('poop')
# print('\n\n')
# model.entryExists('well')
text = "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take Arms against a Sea of troubles, And by opposing end them: to die, to sleep No more; and by a sleep, to say we end The heart-ache, and the thousand natural shocks That Flesh is heir to? 'Tis a consummation Devoutly to be wished."
text = re.sub(r"[^a-zA-Z0-9]+", ' ', text)
result, notPresent, numChanged = model.replaceWords(text)
resultText = " ".join(result)
print("ORIGINAL:\n\t", text)
print("\n\nCHANGED:\n\t", resultText)
if model.debug:
    print("\n\nNOT IN THESAURUS:\n\t", notPresent)
    print("\n\nNUM CHANGED:\n\t", numChanged)