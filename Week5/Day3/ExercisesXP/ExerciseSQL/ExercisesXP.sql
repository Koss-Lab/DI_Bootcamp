-- Exercises XP - DVD Rental

-- 🌟 Exercise 1 : Queries and Table Creation

-- 1. Get a list of all languages
SELECT *
FROM language;

-- 2. Films joined with their languages (title, description, language)
SELECT f.title, f.description, l.name AS language_name
FROM film f
JOIN language l ON f.language_id = l.language_id;

-- 3. All languages, even if no films (LEFT JOIN)
SELECT f.title, f.description, l.name AS language_name
FROM language l
LEFT JOIN film f ON f.language_id = l.language_id;

-- 4. Create a new table "new_film" and insert some rows
DROP TABLE IF EXISTS new_film;
CREATE TABLE new_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO new_film (name) VALUES
('Shinobi Spirit'),
('Lost Horizon'),
('Desert Echoes');

-- 5. Create "customer_review" table with constraints
DROP TABLE IF EXISTS customer_review;
CREATE TABLE customer_review (
    review_id SERIAL PRIMARY KEY,
    film_id INT REFERENCES new_film(id) ON DELETE CASCADE,
    language_id INT REFERENCES language(language_id),
    title VARCHAR(100),
    score INT CHECK (score BETWEEN 1 AND 10),
    review_text TEXT,
    last_update TIMESTAMP DEFAULT NOW()
);

-- 6. Add 2 reviews linked to valid films and languages
INSERT INTO customer_review (film_id, language_id, title, score, review_text)
VALUES
(1, 1, 'Epic ninja battles', 9, 'Really cool movie about ninja spirit.'),
(2, 2, 'Beautiful landscapes', 8, 'Loved the visuals, very artistic.');

-- 7. Delete a film with a review (the review will be deleted automatically by ON DELETE CASCADE)
DELETE FROM new_film
WHERE id = 1;




-- 🌟 Exercise 2 : Updates and Advanced Queries


-- 1. Update the language of some films

UPDATE film
SET language_id = 2
WHERE film_id IN (10, 20);

-- 2. Foreign keys in customer table
-- The customer table references address(address_id).
-- This means when inserting a new customer, a valid address_id must exist.
-- To verify constraints in psql or DataGrip: \d customer

-- 3. Drop the customer_review table

DROP TABLE IF EXISTS customer_review;

-- 4. How many rentals are outstanding (not returned)

SELECT COUNT(*) AS outstanding_rentals
FROM rental
WHERE return_date IS NULL;

-- 5. Find the 30 most expensive outstanding movies

SELECT f.film_id, f.title, f.rental_rate
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NULL
ORDER BY f.rental_rate DESC
LIMIT 30;

-- 6. Friend’s 4 films

-- Film 1: about a sumo wrestler + actor Penelope Monroe

SELECT f.title, f.description
FROM film f
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
WHERE a.first_name = 'Penelope' AND a.last_name = 'Monroe'
  AND f.description ILIKE '%sumo%';

-- Film 2: short documentary (< 60 min), rated "R"

SELECT title, description
FROM film
WHERE length < 60 AND rating = 'R';

-- Film 3: rented by Matthew Mahan, paid > $4, returned between 28 Jul and 1 Aug 2005

SELECT f.title, f.description
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN payment p ON r.rental_id = p.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE c.first_name = 'Matthew' AND c.last_name = 'Mahan'
  AND p.amount > 4
  AND r.return_date BETWEEN '2005-07-28' AND '2005-08-01';

-- Film 4: watched by Matthew Mahan, contains "boat" in title or description, and expensive to replace

SELECT f.title, f.description, f.replacement_cost
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE c.first_name = 'Matthew' AND c.last_name = 'Mahan'
  AND (f.title ILIKE '%boat%' OR f.description ILIKE '%boat%')
ORDER BY f.replacement_cost DESC;
