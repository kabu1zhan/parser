import pymorphy2

morph = pymorphy2.MorphAnalyzer()

slovo = morph.parse('Трахать')[0]
for i in slovo.lexeme:
    print(i[0])