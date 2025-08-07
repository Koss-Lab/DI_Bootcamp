#index.py

import json
import os

# 1. Déterminer le chemin vers le fichier
dir_path = os.path.dirname(os.path.realpath(__file__))
json_path = os.path.join(dir_path, 'file.json')  # le fichier fourni dans l'énoncé

# 2. Lire le JSON dans une variable appelée family
with open(json_path, 'r', encoding='utf-8') as f:
    family = json.load(f)

# 3. Afficher les détails des enfants de Jane
print("👶 Jane's children:")
for child in family['children']:
    print(f"- {child['firstName']}, {child['age']} years old")

# 4. Ajouter une clé 'favorite_color' pour chaque enfant
family['children'][0]['favorite_color'] = 'blue'
family['children'][1]['favorite_color'] = 'green'

# 5. Réécrire dans le fichier JSON avec indent=2
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(family, f, indent=2)

print("✅ JSON file updated with favorite colors.")