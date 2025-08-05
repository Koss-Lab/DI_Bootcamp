#DailyChallenge2.py

from translate import Translator

french_words = ["Bonjour", "Au revoir", "Bienvenue", "A bientôt"]
translator = Translator(from_lang="fr", to_lang="en")

translated_dict = {}

for word in french_words:
    translated = translator.translate(word)
    translated_dict[word] = translated

print(translated_dict)
