-- 🌟 Exercise 1 : DVD Rental (use dvdrental database)

-- 1. How many films for each rating
SELECT rating, COUNT(*) AS total_films
FROM film
GROUP BY rating;

-- 2. Movies with rating G or PG-13
SELECT title, rating
FROM film
WHERE rating IN ('G','PG-13');

-- 3. Movies G or PG-13, under 2h, rental_rate < 3.00, sorted alphabetically
SELECT title, rating, length, rental_rate
FROM film
WHERE rating IN ('G','PG-13')
  AND length < 120
  AND rental_rate < 3.00
ORDER BY title ASC;

-- 4. Update a customer with your details
UPDATE customer
SET first_name = 'Ariel', last_name = 'Kossmann', email = 'ariel@example.com'
WHERE customer_id = 1;

-- 5. Update the address of the same customer
UPDATE address
SET address = '123 Tel Aviv Street', phone = '0500000000'
WHERE address_id = (
    SELECT address_id FROM customer WHERE customer_id = 1
);



-- 🌟 Exercise 2 : Students table (use public database)

-- 1. Update birthdates of twins (Marc + Lea Benichou)
UPDATE students
SET birth_date = '1998-11-02'
WHERE first_name IN ('Marc','Lea') AND last_name = 'Benichou';

-- 2. Change David’s last_name from Grez to Guez
UPDATE students
SET last_name = 'Guez'
WHERE first_name = 'David' AND last_name = 'Grez';

-- 3. Delete Lea Benichou
DELETE FROM students
WHERE first_name = 'Lea' AND last_name = 'Benichou';

-- 4. Count how many students
SELECT COUNT(*) AS total_students
FROM students;

-- 5. Count students born after 2000-01-01
SELECT COUNT(*) AS born_after_2000
FROM students
WHERE birth_date > '2000-01-01';

-- 6. Add new column math_grade
ALTER TABLE students
ADD COLUMN math_grade INT;

-- 7. Add grades
UPDATE students SET math_grade = 80 WHERE id = 1;
UPDATE students SET math_grade = 90 WHERE id IN (2,4);
UPDATE students SET math_grade = 40 WHERE id = 6;

-- 8. Count students with grade > 83
SELECT COUNT(*) AS above_83
FROM students
WHERE math_grade > 83;

-- 9. Insert duplicate Omer Simpson with new grade
INSERT INTO students (first_name, last_name, birth_date, math_grade)
VALUES ('Omer','Simpson','1980-10-03',70);

-- 10. Count how many grades each student has
SELECT first_name, last_name, COUNT(math_grade) AS total_grade
FROM students
GROUP BY first_name, last_name;

-- 11. Sum of all grades
SELECT SUM(math_grade) AS sum_grades
FROM students;



-- 🌟 Exercise 3 : Items and Customers (use public database)

-- Part I: Create purchases table
DROP TABLE IF EXISTS purchases;

CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    item_id INT REFERENCES items(item_id),
    quantity_purchased INT
);

-- Insert purchases with subqueries
INSERT INTO purchases (customer_id, item_id, quantity_purchased)
VALUES (
    (SELECT customer_id FROM customers WHERE first_name='Scott' AND last_name='Scott'),
    (SELECT item_id FROM items WHERE name='Fan'),
    1
);

INSERT INTO purchases (customer_id, item_id, quantity_purchased)
VALUES (
    (SELECT customer_id FROM customers WHERE first_name='Melanie' AND last_name='Johnson'),
    (SELECT item_id FROM items WHERE name='Large Desk'),
    10
);

INSERT INTO purchases (customer_id, item_id, quantity_purchased)
VALUES (
    (SELECT customer_id FROM customers WHERE first_name='Greg' AND last_name='Jones'),
    (SELECT item_id FROM items WHERE name='Small Desk'),
    2
);

-- Part II: Queries on purchases

-- 1. All purchases
SELECT * FROM purchases;

-- 2. All purchases joined with customers
SELECT p.id, c.first_name, c.last_name, p.item_id, p.quantity_purchased
FROM purchases p
JOIN customers c ON p.customer_id = c.customer_id;

-- 3. Purchases of customer with ID = 5
SELECT * FROM purchases
WHERE customer_id = 5;

-- 4. Purchases for large desk AND small desk
SELECT * FROM purchases
WHERE item_id IN (
    SELECT item_id FROM items WHERE name IN ('Large Desk','Small Desk')
);

-- 5. Show all customers who made a purchase (with item name)
SELECT c.first_name, c.last_name, i.name AS item_name
FROM purchases p
JOIN customers c ON p.customer_id = c.customer_id
JOIN items i ON p.item_id = i.item_id;

-- 6. Try inserting a row with customer but no item
INSERT INTO purchases (customer_id, item_id, quantity_purchased)
VALUES (1, NULL, 1);
-- ⚠️ This will fail because item_id has a FOREIGN KEY constraint (cannot be NULL).
