-- Command: docker exec -it postgres psql -U myuser mydb
-- This command will open the postgres shell, then run the following sql

-- Main Example from Book

CREATE TABLE fashion_sales (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(50),
    sales_amount DECIMAL(10, 2),
    sales_date DATE,
    store_location VARCHAR(100),
    customer_age_group VARCHAR(50),
    campaign_name VARCHAR(100)
);

INSERT INTO fashion_sales (product_name, category, sales_amount, sales_date, store_location, customer_age_group, campaign_name)
VALUES
    ('Slim Fit Jeans', 'Denim', 89.99, '2024-03-01', 'New York', '18-24', 'Spring Launch'),
    ('Leather Jacket', 'Outerwear', 249.99, '2024-03-01', 'Los Angeles', '25-34', 'Spring Launch'),
    ('Graphic T-Shirt', 'Tops', 39.99, '2024-03-02', 'Chicago', '18-24', 'March Madness'),
    ('Summer Dress', 'Dresses', 129.99, '2024-03-03', 'New York', '35-44', 'March Madness'),
    ('Casual Sneakers', 'Footwear', 99.99, '2024-03-03', 'Los Angeles', '25-34', 'Spring Launch');

-- Second Example for Additional Practice

CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(50),
    sales_amount DECIMAL(10, 2),
    sales_date DATE
);

INSERT INTO sales_data (product_name, category, sales_amount, sales_date)
VALUES
    ('Product A', 'Electronics', 1000.50, '2024-03-01'),
    ('Product B', 'Clothing', 750.25, '2024-03-02'),
    ('Product C', 'Home Goods', 1200.75, '2024-03-03'),
    ('Product D', 'Electronics', 900.00, '2024-03-04'),
    ('Product E', 'Clothing', 600.50, '2024-03-05');

-- Generating 1000 more records for fashion_sales
INSERT INTO fashion_sales (product_name, category, sales_amount, sales_date, store_location, customer_age_group, campaign_name) VALUES
('Silk Scarf', 'Accessories', 303.3, '2025-04-23', 'Phoenix', '55-64', 'Spring Launch'),
('Leather Jacket', 'Accessories', 76.52, '2024-06-29', 'Los Angeles', '65+', 'Spring Launch'),
('Designer Handbag', 'Footwear', 308.23, '2024-08-04', 'San Diego', '35-44', 'Back to School'),
('Silk Scarf', 'Tops', 37.18, '2025-12-01', 'Chicago', '55-64', 'Back to School'),
('Silk Scarf', 'Accessories', 87.97, '2024-03-05', 'Dallas', '18-24', 'March Madness');

-- Generating 1000 more records for sales_data
INSERT INTO sales_data (product_name, category, sales_amount, sales_date) VALUES
('Product R', 'Home Goods', 1006.17, '2025-04-18'),
('Product Q', 'Toys', 1920.1, '2024-01-09'),
('Product S', 'Home Goods', 1893.17, '2024-11-29'),
('Product Q', 'Electronics', 2152.8, '2024-06-14'),
('Product S', 'Toys', 2495.22, '2024-12-31');

-- \q to quit the postgres shell