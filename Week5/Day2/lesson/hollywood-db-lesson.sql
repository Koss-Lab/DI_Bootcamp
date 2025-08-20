-- CRÉER LA TABLE

DROP TABLE IF EXISTS actors;
CREATE TABLE actors (
actor_id SERIAL PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(100) NOT NULL,
age DATE NOT NULL,
number_oscars SMALLINT NOT NULL
);

-- INSÉRER UN ACTEUR
INSERT INTO actors (first_name, last_name, age, number_oscars)
VALUES ('Matt', 'Damon', '1970-10-08', 5);

-- RÉCUPÉRER TOUTES LES LIGNES
SELECT * FROM actors;

-- INSÉRER PLUSIEURS D’UN COUP
INSERT INTO actors (first_name, last_name, age, number_oscars)
VALUES
('George', 'Clooney', '1961-05-06', 2),
('Gal', 'Gadot', '1985-04-30', 2),
('Meryl', 'Streep', '1949-06-22', 12),
('Brad', 'Pitt', '1963-12-18', 2);

-- FAIRE UNE RECHERCHE
SELECT first_name, number_oscars
FROM actors
WHERE last_name ILIKE '%mon%';

-- RÉCUPÉRER TOUTES LES LIGNES
SELECT * FROM actors;