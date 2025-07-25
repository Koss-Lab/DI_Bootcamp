#ExercisesXP+.py

student_grades = {
    "Alice": [88, 92, 100],
    "Bob": [75, 78, 80],
    "Charlie": [92, 90, 85],
    "Dana": [83, 88, 92],
    "Eli": [78, 80, 72]
}

student_averages = {}
for name, grades in student_grades.items():
    average = sum(grades) / len(grades)
    student_averages[name] = average

student_letter_grades = {}
for name, avg in student_averages.items():
    if avg >= 90:
        grade = 'A'
    elif avg >= 80:
        grade = 'B'
    elif avg >= 70:
        grade = 'C'
    elif avg >= 60:
        grade = 'D'
    else:
        grade = 'F'
    student_letter_grades[name] = grade

class_average = sum(student_averages.values()) / len(student_averages)

print("Class average:", round(class_average, 2))
print()

max_name_length = max(len(name) for name in student_grades.keys())
for name in student_grades.keys():
    spaces = ' ' * (max_name_length - len(name))
    print(f"{name}:{spaces} Average = {student_averages[name]:.2f}, Grade = {student_letter_grades[name]}")

#Exercise 2

sales_data = [
    {"customer_id": 1, "product": "Smartphone", "price": 600, "quantity": 1, "date": "2023-04-03"},
    {"customer_id": 2, "product": "Laptop", "price": 1200, "quantity": 1, "date": "2023-04-04"},
    {"customer_id": 1, "product": "Laptop", "price": 1000, "quantity": 1, "date": "2023-04-05"},
    {"customer_id": 2, "product": "Smartphone", "price": 500, "quantity": 2, "date": "2023-04-06"},
    {"customer_id": 3, "product": "Headphones", "price": 150, "quantity": 4, "date": "2023-04-07"},
    {"customer_id": 3, "product": "Smartphone", "price": 550, "quantity": 1, "date": "2023-04-08"},
    {"customer_id": 1, "product": "Headphones", "price": 100, "quantity": 2, "date": "2023-04-09"},
]

total_sales = {}
for transaction in sales_data:
    product = transaction["product"]
    total = transaction["price"] * transaction["quantity"]
    total_sales[product] = total_sales.get(product, 0) + total

customer_spending = {}
for transaction in sales_data:
    customer_id = transaction["customer_id"]
    total = transaction["price"] * transaction["quantity"]
    customer_spending[customer_id] = customer_spending.get(customer_id, 0) + total

for transaction in sales_data:
    transaction["total_price"] = transaction["price"] * transaction["quantity"]

high_value_transactions = sorted(
    [t for t in sales_data if t["total_price"] > 500],
    key=lambda x: x["total_price"],
    reverse=True
)

purchase_counts = {}
for transaction in sales_data:
    cid = transaction["customer_id"]
    purchase_counts[cid] = purchase_counts.get(cid, 0) + 1
loyal_customers = [cid for cid, count in purchase_counts.items() if count > 2]

average_transaction_value = {}
for product in total_sales:
    total_quantity = sum(t["quantity"] for t in sales_data if t["product"] == product)
    average_transaction_value[product] = total_sales[product] / total_quantity

product_quantities = {}
for t in sales_data:
    product = t["product"]
    product_quantities[product] = product_quantities.get(product, 0) + t["quantity"]
most_popular_product = max(product_quantities, key=product_quantities.get)

print("Total Sales per Product:", total_sales)
print("Customer Spending:", customer_spending)
print("High Value Transactions:", high_value_transactions)
print("Loyal Customers (more than 2 purchases):", loyal_customers)
print("Average Transaction Value per Product:", average_transaction_value)
print("Most Popular Product (by quantity):", most_popular_product)

