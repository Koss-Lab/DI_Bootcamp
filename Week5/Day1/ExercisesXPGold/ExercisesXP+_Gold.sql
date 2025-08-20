DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL
);

INSERT INTO students (first_name, last_name, birth_date) VALUES
('Marc', 'Benichou', '1998-11-02'),
('Yoan', 'Cohen', '2010-12-03'),
('Lea', 'Benichou', '1987-07-27'),
('Amelia', 'Dux', '1996-04-07'),
('David', 'Grez', '2003-06-14'),
('Omer', 'Simpson', '1980-10-03');

INSERT INTO students (first_name, last_name, birth_date)
VALUES ('Ariel', 'Kossmann', '1998-09-23');

INSERT INTO students (first_name, last_name, birth_date) VALUES
('William', 'Shatner', '1955-04-25'),
('Dolly', 'Parton', '1959-11-29');

-- 1. Fetch all the data
SELECT * FROM students;

-- 2. Fetch all first_name and last_name
SELECT first_name, last_name FROM students;

-- 3. Fetch the student where id = 2
SELECT first_name, last_name FROM students WHERE id = 2;

-- 4. Fetch student with last_name = 'Benichou' AND first_name = 'Marc'
SELECT first_name, last_name FROM students
WHERE first_name = 'Marc' AND last_name = 'Benichou';

-- 5. Fetch students with last_name = 'Benichou' OR first_name = 'Marc'
SELECT first_name, last_name FROM students
WHERE first_name = 'Marc' OR last_name = 'Benichou';

-- 6. Fetch students whose first_name contains 'a'
SELECT first_name, last_name FROM students
WHERE first_name ILIKE '%a%';

-- 7. Fetch students whose first_name starts with 'a'
SELECT first_name, last_name FROM students
WHERE first_name ILIKE 'a%';

-- 8. Fetch students whose first_name ends with 'a'
SELECT first_name, last_name FROM students
WHERE first_name ILIKE '%a';

-- 9. Fetch students whose second to last letter of first_name is 'a'
SELECT first_name, last_name FROM students
WHERE first_name LIKE '%a_';

-- 10. Fetch students whose id = 1 OR id = 3
SELECT first_name, last_name FROM students WHERE id IN (1,3);

-- 11. Fetch students born after 2000-01-01
SELECT first_name, last_name, birth_date
FROM students
WHERE birth_date >= '2000-01-01';

SELECT * FROM students;

-- Exercises XP Gold

-- 1. Fetch the first four students, ordered alphabetically by last_name

SELECT first_name, last_name, birth_date
FROM students
ORDER BY last_name ASC
LIMIT 4;

-- 2. Fetch the youngest student

SELECT first_name, last_name, birth_date
FROM students
ORDER BY birth_date DESC
LIMIT 1;

-- 3. Fetch three students, skipping the first two students

SELECT first_name, last_name, birth_date
FROM students
OFFSET 2
LIMIT 3;