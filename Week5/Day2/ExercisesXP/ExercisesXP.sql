-- 🌟 Exercise 1 : Items and Customers (public database)
-- Run these queries in the database: public

-- 1. All items, ordered by price (lowest to highest)
SELECT * FROM items
ORDER BY price ASC;

-- 2. Items with price >= 80, ordered by price (highest to lowest)
SELECT * FROM items
WHERE price >= 80
ORDER BY price DESC;

-- 3. First 3 customers in alphabetical order of first_name (exclude PK)
SELECT first_name, last_name
FROM customers
ORDER BY first_name ASC
LIMIT 3;

-- 4. All last names only, in reverse alphabetical order
SELECT last_name
FROM customers
ORDER BY last_name DESC;



-- 🌟 Exercise 2 : dvdrental database
-- Run these queries in the database: dvdrental

-- 1. Select all columns from "customer"
SELECT * FROM customer;

-- 2. Display full name using alias
SELECT first_name || ' ' || last_name AS full_name
FROM customer;

-- 3. Get all create_date (no duplicates)
SELECT DISTINCT create_date
FROM customer;

-- 4. All customer details, ordered by first_name (Z → A)
SELECT * FROM customer
ORDER BY first_name DESC;

-- 5. Film info (id, title, description, release_year, rental_rate) ordered by rental_rate (ASC)
SELECT film_id, title, description, release_year, rental_rate
FROM film
ORDER BY rental_rate ASC;

-- 6. Address + phone of customers in district = 'Texas'
SELECT address, phone
FROM address
WHERE district = 'Texas';

-- 7. Movie details for film_id = 15 OR 150
SELECT * FROM film
WHERE film_id IN (15,150);

-- 8. Check if favorite movie exists (example: 'ACADEMY DINOSAUR')
SELECT film_id, title, description, length, rental_rate
FROM film
WHERE title = 'ACADEMY DINOSAUR';

-- 9. Try fuzzy search (all movies starting with first 2 letters of fav movie, ex: 'AC')
SELECT film_id, title, description, length, rental_rate
FROM film
WHERE title ILIKE 'AC%';

-- 10. Find 10 cheapest movies
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
LIMIT 10;

-- 11. Find next 10 cheapest movies (without LIMIT, use OFFSET)
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
OFFSET 10 LIMIT 10;

-- 12. Join customer + payment (names + amount + date), ordered by customer_id
SELECT c.first_name, c.last_name, p.amount, p.payment_date
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY c.customer_id;

-- 13. Movies not in inventory
SELECT *
FROM film
WHERE film_id NOT IN (
    SELECT DISTINCT film_id FROM inventory
);

-- 14. Find which city is in which country
SELECT ci.city, co.country
FROM city ci
JOIN country co ON ci.country_id = co.country_id;

-- 15. BONUS: Seller performance (customer id, names, amount, date, ordered by staff_id)
SELECT c.customer_id, c.first_name, c.last_name, p.amount, p.payment_date, p.staff_id
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY p.staff_id, c.customer_id;
