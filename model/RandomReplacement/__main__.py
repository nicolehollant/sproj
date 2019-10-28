from RandomReplacement.model import Model
import re

model = Model(ignoreArticles=False)
# print('\n\n')
# model.entryExists('well')
# text = "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take Arms against a Sea of troubles, And by opposing end them: to die, to sleep No more; and by a sleep, to say we end The heart-ache, and the thousand natural shocks That Flesh is heir to? 'Tis a consummation Devoutly to be wished."
text = "Freeman and slave, patrician and plebeian, lord and serf, guild-master and journeyman, in a word, oppressor and oppressed, stood in constant opposition to one another, carried on an uninterrupted, now hidden, now open fight, a fight that each time ended, either in a revolutionary re-constitution of society at large, or in the common ruin of the contending classes. \n In the earlier epochs of history, we find almost everywhere a complicated arrangement of society into various orders, a manifold gradation of social rank.  In ancient Rome we have patricians, knights, plebeians, slaves; in the Middle Ages, feudal lords, vassals, guild-masters, journeymen, apprentices, serfs; in almost all of these classes, again, subordinate gradations."
text = re.sub(r"[^a-zA-Z0-9]+", ' ', text)
result, notPresent, numChanged = model.replaceWords(text)
resultText = " ".join(result)
print("ORIGINAL:\n\t", text)
print("\n\nCHANGED:\n\t", resultText)
if model.debug:
    print("\n\nNOT IN THESAURUS:\n\t", notPresent)
    print("\n\nNUM CHANGED:\n\t", numChanged)