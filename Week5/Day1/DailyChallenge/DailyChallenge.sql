-- 1. Count how many actors are in the table
SELECT COUNT(*) AS total_actors
FROM actors;

-- 2. Try to insert an actor with blank fields
-- This will fail because columns are NOT NULL
INSERT INTO actors (first_name, last_name, age, number_oscars)
VALUES ('Test', NULL, NULL, NULL);