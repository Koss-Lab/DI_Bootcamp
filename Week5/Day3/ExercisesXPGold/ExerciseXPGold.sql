-- Exercises XP Gold - DVD Rental
-- Database: dvdrental
-- Date: 2025-03-06
-- Author: Ariel Kossmann


-- Exercise 1 : Rentals & Action films

-- 1. Rentals which are out (not returned yet)
-- Identified by return_date IS NULL
SELECT r.rental_id, r.rental_date, f.title, c.first_name, c.last_name
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN customer c ON r.customer_id = c.customer_id
WHERE r.return_date IS NULL;

-- 2. Customers who have not returned rentals (grouped)
SELECT c.customer_id, c.first_name, c.last_name, COUNT(*) AS outstanding_rentals
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
WHERE r.return_date IS NULL
GROUP BY c.customer_id, c.first_name, c.last_name;

-- 3. List of Action films with Joe Swank
-- (Join film → film_category → category + film_actor → actor)
SELECT f.title, f.description
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
WHERE cat.name = 'Action'
  AND a.first_name = 'Joe'
  AND a.last_name = 'Swank';

-- Note: Shortcut idea = create a VIEW that joins film, category, actor
-- to quickly filter films by category/actor combinations.


-- Exercise 2 : Happy Halloween

-- 1. How many stores + their city and country
SELECT s.store_id, ci.city, co.country
FROM store s
JOIN address a ON s.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id;

-- 2. Total viewing time (sum of film lengths) for each store
-- Only count rentals that were actually returned
SELECT s.store_id, SUM(f.length) AS total_minutes,
       ROUND(SUM(f.length) / 60.0, 2) AS total_hours,
       ROUND(SUM(f.length) / 1440.0, 2) AS total_days
FROM store s
JOIN inventory i ON s.store_id = i.store_id
JOIN film f ON i.film_id = f.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
WHERE r.return_date IS NOT NULL
GROUP BY s.store_id;

-- 3. All customers in the cities where stores are located
SELECT DISTINCT c.customer_id, c.first_name, c.last_name, ci.city
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
WHERE ci.city_id IN (
    SELECT ci2.city_id
    FROM store s
    JOIN address a2 ON s.address_id = a2.address_id
    JOIN city ci2 ON a2.city_id = ci2.city_id
);

-- 4. All customers in the countries where stores are located
SELECT DISTINCT c.customer_id, c.first_name, c.last_name, co.country
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
WHERE co.country_id IN (
    SELECT co2.country_id
    FROM store s
    JOIN address a2 ON s.address_id = a2.address_id
    JOIN city ci2 ON a2.city_id = ci2.city_id
    JOIN country co2 ON ci2.country_id = co2.country_id
);

-- 5. "Safe list" of movies (exclude Horror and scary words)
SELECT f.film_id, f.title, f.description, f.length
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
WHERE cat.name <> 'Horror'
  AND f.title NOT ILIKE ANY (ARRAY['%beast%','%monster%','%ghost%','%dead%','%zombie%','%undead%'])
  AND f.description NOT ILIKE ANY (ARRAY['%beast%','%monster%','%ghost%','%dead%','%zombie%','%undead%']);

-- Sum of their viewing time in minutes, hours, days
SELECT SUM(f.length) AS total_minutes,
       ROUND(SUM(f.length) / 60.0, 2) AS total_hours,
       ROUND(SUM(f.length) / 1440.0, 2) AS total_days
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
WHERE cat.name <> 'Horror'
  AND f.title NOT ILIKE ANY (ARRAY['%beast%','%monster%','%ghost%','%dead%','%zombie%','%undead%'])
  AND f.description NOT ILIKE ANY (ARRAY['%beast%','%monster%','%ghost%','%dead%','%zombie%','%undead%']);
