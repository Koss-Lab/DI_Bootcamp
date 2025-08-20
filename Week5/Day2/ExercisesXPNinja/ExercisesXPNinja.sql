-- 🌟 Exercise 1 : Bonus Public Database (Continuation of XP)

-- 1. Fetch the last 2 customers in alphabetical order (A-Z), exclude id
SELECT first_name, last_name
FROM customers
ORDER BY first_name ASC
LIMIT 2 OFFSET (
    SELECT COUNT(*) - 2 FROM customers
);

-- 2. Delete all purchases made by Scott
DELETE FROM purchases
WHERE customer_id = (
    SELECT customer_id FROM customers
    WHERE first_name = 'Scott' AND last_name = 'Scott'
);


-- 3. Check if Scott still exists in customers table
SELECT * FROM customers
WHERE first_name = 'Scott' AND last_name = 'Scott';


-- 4. Show all purchases, LEFT JOIN with customers
-- (Scott’s order will appear, but his name will be NULL/blank)
SELECT p.id, p.item_id, p.quantity_purchased, c.first_name, c.last_name
FROM purchases p
LEFT JOIN customers c ON p.customer_id = c.customer_id;


-- 5. Show all purchases, INNER JOIN with customers
-- (Scott’s order will NOT appear, because INNER JOIN only keeps matches)
SELECT p.id, p.item_id, p.quantity_purchased, c.first_name, c.last_name
FROM purchases p
INNER JOIN customers c ON p.customer_id = c.customer_id;
