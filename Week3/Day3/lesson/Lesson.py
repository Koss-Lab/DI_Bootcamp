#lesson.py

import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print('dir path: ', dir_path)

with open(f'{dir_path}/secret.txt', 'r', encoding='utf-8') as file_obj:
    file_content = file_obj.read()

    print(file_content)

#Exercise

with open(f'{dir_path}/star_wars.txt', 'r', encoding='utf-8') as f:
    txtlist = f.readlines()
    for line in txtlist:
        print(line)
print('end of document')

print(txtlist[4])
print(txtlist[0][:4])

for line in txtlist:
    words = line.strip().split()
    for word in words:
        print(list(word))

# 5. Compter "Darth", "Luke", "Lea"
count_darth = 0
count_luke = 0
count_lea = 0

for line in txtlist:
    count_darth += line.count("Darth")
    count_luke += line.count("Luke")
    count_lea += line.count("Lea")

print("Darth:", count_darth)
print("Luke:", count_luke)
print("Lea:", count_lea)

with open(f'{dir_path}/star_wars.txt', 'a', encoding='utf-8') as f:
    f.write("\nAriel\n")

with open(f'{dir_path}/star_wars.txt', 'r', encoding='utf-8') as f:
    txtlist = f.readlines()

modified_lines = []
for line in txtlist:
    if line.strip() == "Luke":
        modified_lines.append('Luke Skywalker\n')
    else:
        modified_lines.append(line)

with open(f'{dir_path}/star_wars.txt', 'w', encoding='utf-8') as f:
    f.writelines(modified_lines)


with open(f'{dir_path}/star_wars.txt', 'r', encoding='utf-8') as f:
    txtlist = f.readlines()

modified_lines = []
for line in txtlist:
    if line.strip() == "Darth":
        modified_lines.append('Darth Vader\n')
    else:
        modified_lines.append(line)

with open(f'{dir_path}/star_wars.txt', 'w', encoding='utf-8') as f:
    f.writelines(modified_lines)


dir_path = os.path.dirname(os.path.realpath(__file__))
my_family = {
    "parents":["Beth","Jerry"],
    "children": ["Summer","Morty"]
}
with open(f"{dir_path}/family.json","w") as f:
     json.dump(my_family, f)
json_my_family_string = json.dumps(my_family)
print(json_my_family_string)
#convert from a json file to a dict
with open(f"{dir_path}/family.json","r") as f:
    my_family2 = json.load(f)
print(my_family2)
parsed_family = json.loads(json_my_family_string)
print(type(parsed_family))