#DailyChallenge.py

#exercise 1

word = input("Enter a word: ")
letter_index_dict = {}
for index, letter in enumerate(word):
    if letter in letter_index_dict:
        letter_index_dict[letter].append(index)
    else:
        letter_index_dict[letter] = [index]

print(letter_index_dict)

#Exercise 2

items_purchase = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}
wallet = '300$'

#item_prices = int(item_purchases.replace("$", "").replace(",", ""))
wallet_amount = int(wallet.replace('$', ''))
affordable_items = []

for item, price in items_purchase.items():
    price_value = int(price.replace('$', '').replace(',', ''))
    if price_value <= wallet_amount:
        affordable_items.append(item)

affordable_items = sorted(affordable_items)
if affordable_items:
    print(affordable_items)
else:
    print("Nothing")
