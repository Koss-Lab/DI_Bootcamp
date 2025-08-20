-- Database: hollywood

-- How to create a table

CREATE TABLE actors(
actor_id SERIAL PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR (100) NOT NULL,
age DATE NOT NULL,
number_oscars SMALLINT NOT NULL
)

-- how to insert data into the table

--INSERT INTO actors (first_name, last_name, age, number_oscars)
--VALUES ('Matt', 'Damon', '08/10/1976', 5)

-- How to retrieve data on the table

--SELECT * FROM actors

INSERT INTO actors(first_name, last_name, age, number_oscars)
VALUES ('George', 'Clooney', '06/05/1961', 2),
('Gal', 'Gadot', '30/04/1985', 2),
('Meryl', 'Streep', '22/06/1949', 12);

--SELECT * FROM actors