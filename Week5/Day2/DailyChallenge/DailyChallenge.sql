-- Daily Challenge - SQL Puzzle

-- 1. Create the tables
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



-- Q1
-- Query:
-- SELECT COUNT(*)
-- FROM FirstTab AS ft
-- WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NULL );

-- Explanation:
-- Subquery = empty set, because "WHERE id IS NULL" gives only NULL.
-- NULL is not compared as a value → result is ignored.
-- So the subquery returns nothing.
-- Therefore "NOT IN (empty set)" keeps all rows.
-- FirstTab has 4 rows.
-- Expected answer = 4

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NULL );



-- Q2
-- Query:
-- SELECT COUNT(*)
-- FROM FirstTab AS ft
-- WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id = 5 );

-- Explanation:
-- Subquery = (5).
-- Condition becomes "ft.id NOT IN (5)".
-- Rows left: 6, 7, NULL → 3 rows.
-- Expected answer = 3

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id = 5 );



-- Q3
-- Query:
-- SELECT COUNT(*)
-- FROM FirstTab AS ft
-- WHERE ft.id NOT IN ( SELECT id FROM SecondTab );

-- Explanation:
-- Subquery = (5, NULL).
-- Using NOT IN with NULL → result becomes UNKNOWN for all rows.
-- That means no row satisfies the condition.
-- Expected answer = 0

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab );



-- Q4
-- Query:
-- SELECT COUNT(*)
-- FROM FirstTab AS ft
-- WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NOT NULL );

-- Explanation:
-- Subquery = (5).
-- Condition = "ft.id NOT IN (5)".
-- Rows left: 6, 7, NULL → 3 rows.
-- Expected answer = 3

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NOT NULL );
