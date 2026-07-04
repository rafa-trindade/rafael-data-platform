-- ==========================================
-- SCRIPT DE INICIALIZAÇÃO DO BANCO DE DADOS
-- Projeto: Data Engineering Drill
-- ==========================================

-- Criação do Schema
CREATE SCHEMA IF NOT EXISTS drill_sql_02;
SET search_path TO drill_sql_02, public;

-- 1. Criação das Tabelas
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    price NUMERIC(10,2),
    category_id INTEGER REFERENCES category(category_id)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150)
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    client_id INTEGER REFERENCES users(user_id),
    seller_id INTEGER REFERENCES users(user_id), -- Pode ser nulo para simular erro
    quantity INTEGER,
    total_price NUMERIC(12,2),
    sale_date DATE
);

-- 2. Inserção de Dados - Dimensões
INSERT INTO category (category_id, name) VALUES 
(1, 'Fruits'), (2, 'Bakery'), (3, 'Dairy'), (4, 'Meat'), 
(5, 'Beverages'), (6, 'Snacks'), (7, 'Desserts');

INSERT INTO products (product_id, name, price, category_id) VALUES 
(1, 'Apple', 1.99, 1), (2, 'Banana', 0.99, 1), (3, 'Orange', 1.49, 1),
(4, 'Bread', 2.49, 2), (5, 'Milk', 3.49, 3), (6, 'Eggs', 2.99, 3), 
(7, 'Cheese', 4.99, 3), (8, 'Chicken', 6.99, 4), (9, 'Beef', 8.99, 4), 
(10, 'Pork', 7.99, 4), (11, 'Soda', 1.99, 5), (12, 'Water', 0.99, 5), 
(13, 'Juice', 2.49, 5), (14, 'Chips', 1.99, 6), (15, 'Cookies', 2.49, 6), 
(16, 'Candy', 0.99, 6), (17, 'Ice Cream', 3.49, 7), (18, 'Yogurt', 2.99, 7), 
(19, 'Pudding', 1.99, 7);

INSERT INTO users (user_id, name, email) VALUES 
(1, 'John Doe', 'john.doe@example.com'),
(2, 'Jane Smith', 'jane.smith@example.com'),
(3, 'Michael Jones', 'michael.jones@example.com'),
(4, 'Sarah Miller', 'sarah.miller@example.com'),
(5, 'Robert Brown', 'robert.brown@example.com');

-- 3. Inserção de Dados - Fato (Vendas normais com datas distribuídas)
INSERT INTO sales (sale_id, product_id, client_id, seller_id, quantity, total_price, sale_date) VALUES 
-- Mês 04
(1, 1, 1, 2, 5, 9.95, '2026-04-15'), (2, 2, 2, 1, 3, 2.97, '2026-04-15'),
(3, 3, 3, 2, 2, 2.98, '2026-04-15'), (4, 4, 4, 1, 1, 2.49, '2026-04-15'),
(5, 5, 5, 2, 4, 13.96, '2026-04-15'),
-- Mês 05
(6, 6, 1, 1, 6, 17.94, '2026-05-10'), (7, 7, 2, 2, 3, 14.97, '2026-05-10'),
(8, 8, 3, 1, 2, 13.98, '2026-05-10'), (9, 9, 4, 2, 4, 35.96, '2026-05-10'),
(10, 10, 5, 1, 5, 39.95, '2026-05-10'),
(11, 11, 3, 2, 2, 3.98, '2026-05-25'), (12, 12, 5, 1, 1, 0.99, '2026-05-25'),
(13, 13, 4, 2, 3, 7.47, '2026-05-25'), (14, 14, 3, 1, 4, 7.96, '2026-05-25'),
(15, 15, 4, 2, 5, 12.45, '2026-05-25'),
-- Mês 06
(16, 16, 5, 1, 6, 5.94, '2026-06-05'), (17, 17, 5, 2, 2, 6.98, '2026-06-05'),
(18, 18, 5, 1, 3, 10.47, '2026-06-05'), (19, 19, 4, 2, 4, 13.96, '2026-06-05'),
(20, 19, 5, 1, 5, 9.95, '2026-06-05'); -- Ajustado o ID do produto 20 para 19

-- 4. Injeção de Casos Extremos (Para testes de Data Quality e Nulos)
INSERT INTO sales (sale_id, product_id, client_id, seller_id, quantity, total_price, sale_date) VALUES
(21, 1, 3, NULL, 2, 3.98, '2026-06-10'),   -- Vendedor Nulo (COALESCE)
(22, 2, 4, 1, 10, 50.00, '2026-06-12'),    -- Inconsistência de Preço (Data Quality)
(23, 5, 2, 2, 1, 3.49, '2026-06-15'),      -- Duplicata Exata Linha 1
(24, 5, 2, 2, 1, 3.49, '2026-06-15');      -- Duplicata Exata Linha 2

-- Ajuste do ponteiro das chaves primárias automáticas
SELECT setval('category_category_id_seq', (SELECT MAX(category_id) FROM category));
SELECT setval('products_product_id_seq', (SELECT MAX(product_id) FROM products));
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));
SELECT setval('sales_sale_id_seq', (SELECT MAX(sale_id) FROM sales));