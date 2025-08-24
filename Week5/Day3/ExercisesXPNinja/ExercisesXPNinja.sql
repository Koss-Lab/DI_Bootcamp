-- Exercises XP Ninja - DVD Rental
-- Database: dvdrental
-- Date: 2024-09-13
-- Author: Ariel Kossmann

------------------------------------------------------------
-- Exercise 1 : Encourage families and kids
------------------------------------------------------------

-- 1. Retrieve all films with rating G or PG that are NOT currently rented
-- Logic: a film is available if it is in inventory BUT not in an active rental (return_date IS NULL).
SELECT DISTINCT f.film_id, f.title, f.rating
FROM film f
JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
WHERE f.rating IN ('G','PG')
  AND (r.rental_id IS NULL OR r.return_date IS NOT NULL);

-- 2. Create a waiting list table for children’s movies
DROP TABLE IF EXISTS children_waiting_list;
CREATE TABLE children_waiting_list (
    waiting_id SERIAL PRIMARY KEY,
    film_id INT NOT NULL REFERENCES film(film_id) ON DELETE CASCADE,
    child_name VARCHAR(100) NOT NULL,
    added_date TIMESTAMP DEFAULT NOW()
);

-- 3. Insert some sample rows to test waiting list (safe with ILIKE for titles)
INSERT INTO children_waiting_list (film_id, child_name)
SELECT f.film_id, v.child_name
FROM film f
JOIN (VALUES
    ('Academy Dinosaur','Alice'),
    ('Academy Dinosaur','Ben'),
    ('Ace Goldfinger','Charlie')
) AS v(title, child_name) ON f.title ILIKE v.title;

-- 4. Retrieve the number of people waiting for each children’s DVD
SELECT f.title, COUNT(w.waiting_id) AS waiting_count
FROM children_waiting_list w
JOIN film f ON w.film_id = f.film_id
GROUP BY f.title
ORDER BY waiting_count DESC;
