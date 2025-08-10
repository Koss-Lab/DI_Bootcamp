import requests
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

response = requests.get('https://api.chucknorris.io/jokes/random')

# print(response.text)

data = json.loads(response.text)

print(data['value'])

with open(f'{dir_path}/jokes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, sort_keys=True)