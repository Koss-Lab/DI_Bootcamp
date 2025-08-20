DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS customers;


CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Items
INSERT INTO items (name, price)
VALUES
('Small Desk', 100),
('Large Desk', 300),
('Fan', 80);

-- Customers
INSERT INTO customers (first_name, last_name)
VALUES
('Greg', 'Jones'),
('Sandra', 'Jones'),
('Scott', 'Scott'),
('Trevor', 'Green'),
('Melanie', 'Johnson');

-- 1. All items
SELECT * FROM items;

-- 2. Items with price > 80
SELECT * FROM items WHERE price > 80;

-- 3. Items with price <= 300
SELECT * FROM items WHERE price <= 300;

-- 4. Customers whose last name is 'Smith' (⚠ no result expected)
SELECT * FROM customers WHERE last_name = 'Smith';

-- 5. Customers whose last name is 'Jones'
SELECT * FROM customers WHERE last_name = 'Jones';

-- 6. Customers whose first name is not 'Scott'
SELECT * FROM customers WHERE first_name <> 'Scott';
