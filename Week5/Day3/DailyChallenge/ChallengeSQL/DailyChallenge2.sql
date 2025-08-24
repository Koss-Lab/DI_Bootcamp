-- Daily Challenge - Items and Orders
-- Date: 2024-09-13
-- Database: public
-- Author: Ariel Kossmann

------------------------------------------------------------
-- STEP 1 : Drop old tables (with CASCADE for safety)
------------------------------------------------------------
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS product_orders CASCADE;
DROP TABLE IF EXISTS users CASCADE;

------------------------------------------------------------
-- STEP 2 : Create base tables
------------------------------------------------------------

-- Orders table
CREATE TABLE product_orders (
    order_id SERIAL PRIMARY KEY,
    order_date TIMESTAMP DEFAULT NOW()
);

-- Items table
-- One order → many items
CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES product_orders(order_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

------------------------------------------------------------
-- STEP 3 : Insert sample data
------------------------------------------------------------
INSERT INTO product_orders DEFAULT VALUES; -- order 1
INSERT INTO product_orders DEFAULT VALUES; -- order 2

INSERT INTO items (order_id, name, price) VALUES
(1, 'Banana', 2.50),
(1, 'Apple', 1.20),
(1, 'Chocolate', 3.80),
(2, 'Bread', 4.00),
(2, 'Milk', 2.20);

------------------------------------------------------------
-- STEP 4 : Function → total price for a given order
------------------------------------------------------------
DROP FUNCTION IF EXISTS get_order_total(INT);

CREATE FUNCTION get_order_total(p_order_id INT)
RETURNS NUMERIC AS $$
    SELECT COALESCE(SUM(price),0)
    FROM items
    WHERE order_id = p_order_id;
$$ LANGUAGE SQL;

-- Test
SELECT get_order_total(1) AS total_order_1;  -- expected 7.50
SELECT get_order_total(2) AS total_order_2;  -- expected 6.20


------------------------------------------------------------
-- BONUS : Users and their orders
------------------------------------------------------------

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

-- Add relationship user → product_orders
ALTER TABLE product_orders
ADD COLUMN user_id INT REFERENCES users(user_id);

-- Insert users
INSERT INTO users (username) VALUES
('Alice'),
('Bob');

-- Update existing orders with users
UPDATE product_orders SET user_id = 1 WHERE order_id = 1;
UPDATE product_orders SET user_id = 2 WHERE order_id = 2;

------------------------------------------------------------
-- BONUS Function → total price for a given order of a given user
------------------------------------------------------------
DROP FUNCTION IF EXISTS get_user_order_total(INT, INT);

CREATE FUNCTION get_user_order_total(p_user_id INT, p_order_id INT)
RETURNS NUMERIC AS $$
    SELECT COALESCE(SUM(i.price),0)
    FROM items i
    JOIN product_orders o ON i.order_id = o.order_id
    WHERE o.order_id = p_order_id
      AND o.user_id = p_user_id;
$$ LANGUAGE SQL;

-- Test
SELECT get_user_order_total(1,1) AS alice_order_1; -- expected 7.50
SELECT get_user_order_total(2,2) AS bob_order_2;   -- expected 6.20
