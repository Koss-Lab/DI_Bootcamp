#exercises_xp_ninja.py

car_string = "Volkswagen, Toyota, Ford Motor, Honda, Chevrolet"
manufacturers = car_string.split(", ")
print(f"There are {len(manufacturers)} manufacturers in the list.")

print("\n📦 Manufacturers in descending order (Z-A):")
for company in sorted(manufacturers, reverse=True):
    print("-", company)

count_with_o = sum(1 for name in manufacturers if 'o' in name.lower())
print(f"\n🔎 Number of manufacturers with the letter 'o': {count_with_o}")

count_without_i = sum(1 for name in manufacturers if 'i' not in name.lower())
print(f"🔎 Number of manufacturers without the letter 'i': {count_without_i}")

print("\n Removing duplicates...")
duplicates_list = ["Honda", "Volkswagen", "Toyota", "Ford Motor", "Honda", "Chevrolet", "Toyota"]

unique_companies = list(set(duplicates_list))
unique_companies.sort()

as_string = ", ".join(unique_companies)
print(f"Unique companies ({len(unique_companies)}):")
print(as_string)

print("\n Companies sorted A-Z, but names reversed:")
for name in sorted(unique_companies):
    print(name[::-1])
