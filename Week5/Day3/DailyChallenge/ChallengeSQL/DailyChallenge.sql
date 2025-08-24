-- Daily Challenge - Tables Relationships
-- Date: 2025-03-06
-- Author: Ariel Kossmann
-- Database: public (default)

------------------------------------------------------------
-- PART I : One to One relationship (Customer - Customer Profile)
------------------------------------------------------------

-- Drop old tables if they exist
DROP TABLE IF EXISTS customer_profile;
DROP TABLE IF EXISTS customer;

-- 1. Create Customer table
CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- 2. Create Customer Profile table
CREATE TABLE customer_profile (
    id SERIAL PRIMARY KEY,
    isLoggedIn BOOLEAN DEFAULT FALSE,
    customer_id INT UNIQUE REFERENCES customer(id)
);

-- 3. Insert customers
INSERT INTO customer (first_name, last_name) VALUES
('John', 'Doe'),
('Jerome', 'Lalu'),
('Lea', 'Rive');

-- 4. Insert profiles using subqueries
INSERT INTO customer_profile (isLoggedIn, customer_id)
VALUES
(TRUE, (SELECT id FROM customer WHERE first_name='John' AND last_name='Doe')),
(FALSE, (SELECT id FROM customer WHERE first_name='Jerome' AND last_name='Lalu'));

-- 5. Queries

-- a. First_name of loggedIn customers
SELECT c.first_name
FROM customer c
JOIN customer_profile cp ON c.id = cp.customer_id
WHERE cp.isLoggedIn = TRUE;

-- b. All customers + isLoggedIn status (even without profile)
SELECT c.first_name, cp.isLoggedIn
FROM customer c
LEFT JOIN customer_profile cp ON c.id = cp.customer_id;

-- c. Number of customers not loggedIn
SELECT COUNT(*) AS not_logged_in
FROM customer c
LEFT JOIN customer_profile cp ON c.id = cp.customer_id
WHERE cp.isLoggedIn = FALSE OR cp.isLoggedIn IS NULL;


------------------------------------------------------------
-- PART II : Many to Many relationship (Book - Student - Library)
------------------------------------------------------------

-- Drop old tables if they exist
DROP TABLE IF EXISTS library;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS book;

-- 1. Create Book table
CREATE TABLE book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL
);

-- Insert books
INSERT INTO book (title, author) VALUES
('Alice In Wonderland', 'Lewis Carroll'),
('Harry Potter', 'J.K Rowling'),
('To Kill a Mockingbird', 'Harper Lee');

-- 2. Create Student table
CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    age INT CHECK (age <= 15)
);

-- Insert students
INSERT INTO student (name, age) VALUES
('John', 12),
('Lera', 11),
('Patrick', 10),
('Bob', 14);

-- 3. Create Library (junction table)
CREATE TABLE library (
    book_fk_id INT REFERENCES book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    student_fk_id INT REFERENCES student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    borrowed_date DATE,
    PRIMARY KEY (book_fk_id, student_fk_id, borrowed_date)
);

-- 4. Insert borrow records using subqueries
INSERT INTO library (book_fk_id, student_fk_id, borrowed_date)
VALUES
((SELECT book_id FROM book WHERE title='Alice In Wonderland'),
 (SELECT student_id FROM student WHERE name='John'),
 '2022-02-15'),

((SELECT book_id FROM book WHERE title='To Kill a Mockingbird'),
 (SELECT student_id FROM student WHERE name='Bob'),
 '2021-03-03'),

((SELECT book_id FROM book WHERE title='Alice In Wonderland'),
 (SELECT student_id FROM student WHERE name='Lera'),
 '2021-05-23'),

((SELECT book_id FROM book WHERE title='Harry Potter'),
 (SELECT student_id FROM student WHERE name='Bob'),
 '2021-08-12');

-- 5. Queries

-- a. Select all columns from library
SELECT * FROM library;

-- b. Student name + borrowed book title
SELECT s.name, b.title
FROM library l
JOIN student s ON l.student_fk_id = s.student_id
JOIN book b ON l.book_fk_id = b.book_id;

-- c. Average age of children who borrowed "Alice In Wonderland"
SELECT AVG(s.age) AS avg_age
FROM library l
JOIN student s ON l.student_fk_id = s.student_id
JOIN book b ON l.book_fk_id = b.book_id
WHERE b.title = 'Alice In Wonderland';

-- d. Delete a student and check cascade effect
DELETE FROM student WHERE name = 'Bob';
-- The related records in library are automatically deleted due to ON DELETE CASCADE
