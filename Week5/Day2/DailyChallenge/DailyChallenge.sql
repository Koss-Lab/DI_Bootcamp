-- Daily Challenge - SQL Puzzle (Corrected Final Version)

-- STEP 1 : Create and Populate Tables

DROP TABLE IF EXISTS FirstTab;
CREATE TABLE FirstTab (
    id INTEGER,
    name VARCHAR(10)
);

INSERT INTO FirstTab VALUES
(5,'Pawan'),
(6,'Sharlee'),
(7,'Krish'),
(NULL,'Avtaar');

SELECT * FROM FirstTab;

-- Expected output (FirstTab):
-- id   | name
-- 5    | Pawan
-- 6    | Sharlee
-- 7    | Krish
-- NULL | Avtaar


DROP TABLE IF EXISTS SecondTab;
CREATE TABLE SecondTab (
    id INTEGER
);

INSERT INTO SecondTab VALUES
(5),
(NULL);

SELECT * FROM SecondTab;

-- Expected output (SecondTab):
-- id
-- 5
-- NULL



-- STEP 2 : Queries and Explanations

-- Q1
-- Query: Count rows in FirstTab where id NOT IN (SELECT id FROM SecondTab WHERE id IS NULL)
-- Subquery = [NULL]
-- Condition: id NOT IN (NULL) → always UNKNOWN
-- Since WHERE only keeps rows where condition is TRUE, no rows are returned.
-- Expected answer = 0
SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NULL );


-- Q2
-- Query: Count rows where id NOT IN (SELECT id FROM SecondTab WHERE id = 5)
-- Subquery = [5]
-- Condition: id NOT IN (5)
-- - id=5 → FALSE (excluded)
-- - id=6, id=7 → TRUE (kept)
-- - id=NULL → UNKNOWN (excluded)
-- Rows kept = 2 (id=6, id=7)
-- Expected answer = 2
SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id = 5 );


-- Q3
-- Query: Count rows where id NOT IN (SELECT id FROM SecondTab)
-- Subquery = [5, NULL]
-- Condition: id NOT IN (5, NULL)
-- Because NULL is in the list, every comparison becomes UNKNOWN
-- No rows are kept.
-- Expected answer = 0
SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab );


-- Q4
-- Query: Count rows where id NOT IN (SELECT id FROM SecondTab WHERE id IS NOT NULL)
-- Subquery = [5]
-- Condition: id NOT IN (5)
-- - id=5 → FALSE (excluded)
-- - id=6, id=7 → TRUE (kept)
-- - id=NULL → UNKNOWN (excluded)
-- Rows kept = 2 (id=6, id=7)
-- Expected answer = 2
SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NOT NULL );
