#Dictionaries.py

dict_constructor = {"name":"David",
                    "age": 23,
                    "pets": ["Doudou"]}
student_info = {
    "first_name": "Harry",
    "last_name": "Potter",
    "age": 14,
    "address": "Privet Drive, 4",
    "pets": ["Hedwig","Buckbeak",],
    "houses": {"main":"Griffyndor", "second": "Slytherin"},
    "best_friends": ("Ron Weasley", "Hermione Granger")
}
 #ACCESSING DATA

print(student_info["pets"])
print(student_info["pets"][1])
print(student_info["pets"])

#using methods on the values

student_info["pets"].append("Fenix")
print(student_info["pets"])
print(student_info["first_name"].upper())

#Changing values

student_info["address"] = "Hogwarts"
print(student_info)

#deleting a key

del student_info["age"]
print(student_info)

#creating key value pair

student_info["teachers"] = {"Dumbledore", "Snap", "McGonagal"}
print(student_info)

#Loops and built-in methods for dictionaries
for k in student_info.keys():
    print(k)

#values

for v in student_info.values():
    print(v)
for key, value in student_info.items():
    print(key, value)

#update() method

student_info.update({"patronum": "stag"})
print(student_info)
names = ["Juliana", "Yosef", "Sonia"]
addresses = ["Ramat Gan", "Jerusalem", "Tel Aviv"]
print(list(zip(names,addresses)))
topics = ("Math","Grammar","History", "Sport")
grades = (85, 90, 100, 75, 87, 55, 25)
print(dict(zip(topics, grades)))

sample_dict = {
   "class":{
      "student":{
         "name":"Mike",
         "marks":{
            "physics":70,
            "history":80
         }
      }
   }
}
print(sample_dict["class"]["student"]["marks"]["history"])
sample_dict2 = {
  "name": "Kelly",
  "age":25,
  "salary": 8000,
  "city": "New york"
}
keys_to_remove = ["name", "salary"]
#for key in sample_dict2.keys():
    #if key in keys_to_remove:
       #  del sample_dict2[key]
#print(sample_dict)






