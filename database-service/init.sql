-- Create user roles table
CREATE TABLE IF NOT EXISTS user_roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(20) UNIQUE NOT NULL
);

-- Create user table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES user_roles(id)
);

-- Create tables for the authentication service
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customername VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    account_created_date DATE DEFAULT CURRENT_DATE
);


-- Create a table for product categories
CREATE TABLE IF NOT EXISTS product_categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

-- Create tables for the product service, including a reference to categories
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES product_categories (category_id)
);

-- Create table for product images
CREATE TABLE IF NOT EXISTS product_images (
    image_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Create table for order status
CREATE TABLE IF NOT EXISTS order_status (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create tables for the order service
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (status_id) REFERENCES order_status (status_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Create tables for the cart service
CREATE TABLE IF NOT EXISTS carts (
    cart_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES carts (cart_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Insert initial data into user_roles table
INSERT INTO user_roles (role_name) VALUES 
('superadmin'),
('admin'),
('manager');

-- Insert initial data into users table
INSERT INTO users (username, email, password, role_id) VALUES 
('user1', 'user1@example.com', 'password1', 1),
('user2', 'user2@example.com', 'password2', 2),
('user3', 'user3@example.com', 'password3', 3);


-- Add data to the customers table
INSERT INTO customers (customername, password, email, telephone, account_created_date) VALUES
    ('customer1', 'password1', 'customer1@example.com', '1234567890', CURRENT_DATE),
    ('customer2', 'password2', 'customer2@example.com', '9876543210', CURRENT_DATE),
    ('customer3', 'password3', 'customer3@example.com', '5555555555', CURRENT_DATE),
    ('customer4', 'password4', 'customer4@example.com', '9999999999', CURRENT_DATE),
    ('customer5', 'password5', 'customer5@example.com', '8888888888', CURRENT_DATE),
    ('customer6', 'password6', 'customer6@example.com', '7777777777', CURRENT_DATE),
    ('customer7', 'password7', 'customer7@example.com', '6666666666', CURRENT_DATE),
    ('customer8', 'password8', 'customer8@example.com', '4444444444', CURRENT_DATE),
    ('customer9', 'password9', 'customer9@example.com', '3333333333', CURRENT_DATE),
    ('customer10', 'password10', 'customer10@example.com', '2222222222', CURRENT_DATE),
    ('customer11', 'password11', 'customer11@example.com', '1111111111', CURRENT_DATE),
    ('customer12', 'password12', 'customer12@example.com', '9999999990', CURRENT_DATE),
    ('customer13', 'password13', 'customer13@example.com', '8888888880', CURRENT_DATE),
    ('customer14', 'password14', 'customer14@example.com', '7777777770', CURRENT_DATE),
    ('customer15', 'password15', 'customer15@example.com', '6666666660', CURRENT_DATE);


-- Add data to the categories table
INSERT INTO product_categories (name, description) VALUES
    ('Jeans', 'Comfortable and stylish jeans'),
    ('Sneakers', 'Durable and fashionable sneakers'),
    ('Skirts', 'Elegant and versatile skirts'),
    ('Jackets', 'Stylish jackets for all weathers'),
    ('T-Shirts', 'Casual wear for everyday');

-- Insert predefined status values
INSERT INTO order_status (status_name) VALUES
    ('Pending'),
    ('Packed'),
    ('Dispatched'),
    ('Delivered'),
    ('Returned');

-- Add data to the products table, now including category_id
INSERT INTO products (category_id, name, description, price, available) VALUES
    (('5'), 'Product 1', 'Description for Product 1', 10.99, TRUE),
    (('1'), 'Product 2', 'Description for Product 2', 20.49, TRUE),
    (('2'), 'Product 3', 'Description for Product 3', 15.79, TRUE),
    (('3'), 'Product 4', 'Description for Product 4', 30.99, TRUE),
    (('4'), 'Product 5', 'Description for Product 5', 25.99, TRUE),
    (('5'), 'Product 6', 'Description for Product 6', 12.99, TRUE),
    (('1'), 'Product 7', 'Description for Product 7', 18.49, TRUE),
    (('2'), 'Product 8', 'Description for Product 8', 22.79, TRUE),
    (('3'), 'Product 9', 'Description for Product 9', 35.99, TRUE),
    (('4'), 'Product 10', 'Description for Product 10', 29.99, TRUE),
    (('5'), 'Product 11', 'Description for Product 11', 14.99, TRUE),
    (('1'), 'Product 12', 'Description for Product 12', 27.49, TRUE),
    (('2'), 'Product 13', 'Description for Product 13', 19.79, TRUE),
    (('3'), 'Product 14', 'Description for Product 14', 32.99, TRUE),
    (('4'), 'Product 15', 'Description for Product 15', 23.99, TRUE);

    -- Add data to the product_images table
INSERT INTO product_images (product_id, image_url) VALUES
    (1, 'image1.png'),
    (2, 'image2.png'),
    (3, 'image3.png'),
    (4, 'image4.png'),
    (5, 'image5.png'),
    (6, 'image6.png'),
    (7, 'image7.png'),
    (8, 'image8.png'),
    (9, 'image9.png'),
    (10, 'image10.png'),
    (11, 'image11.png'),
    (12, 'image12.png'),
    (13, 'image13.png'),
    (14, 'image14.png'),
    (15, 'image15.png');

    
-- Add data to the orders table
INSERT INTO orders (customer_id, order_date, status_id) VALUES
    (1, CURRENT_TIMESTAMP, '5'),
    (2, CURRENT_TIMESTAMP, '1'),
    (3, CURRENT_TIMESTAMP, '2'),
    (4, CURRENT_TIMESTAMP, '1'),
    (5, CURRENT_TIMESTAMP, '2'),
    (1, CURRENT_TIMESTAMP, '4'),
    (2, CURRENT_TIMESTAMP, '4'),
    (3, CURRENT_TIMESTAMP, '1'),
    (4, CURRENT_TIMESTAMP, '3'),
    (5, CURRENT_TIMESTAMP, '4'),
    (1, CURRENT_TIMESTAMP, '1'),
    (2, CURRENT_TIMESTAMP, '1'),
    (3, CURRENT_TIMESTAMP, '4'),
    (4, CURRENT_TIMESTAMP, '2'),
    (5, CURRENT_TIMESTAMP, '1');

-- Add data to the order_items table
INSERT INTO order_items (order_id, product_id, quantity) VALUES
    (1, 1, 2),
    (2, 3, 1),
    (3, 2, 3),
    (4, 4, 2),
    (5, 5, 1),
    (6, 6, 2),
    (7, 7, 1),
    (8, 8, 3),
    (9, 9, 2),
    (10, 10, 1),
    (11, 11, 3),
    (12, 12, 2),
    (13, 13, 1),
    (14, 14, 2),
    (15, 15, 3);

-- Add data to the carts table
INSERT INTO carts (customer_id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5),
    (1),
    (2),
    (3),
    (4),
    (5),
    (1),
    (2),
    (3),
    (4),
    (5);

-- Add data to the cart_items table
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
    (1, 2, 1),
    (2, 4, 2),
    (3, 1, 3),
    (4, 3, 1),
    (5, 5, 2),
    (6, 6, 1),
    (7, 8, 2),
    (8, 10, 3),
    (9, 12, 1),
    (10, 14, 2),
    (11, 1, 1),
    (12, 3, 2),
    (13, 5, 3),
    (14, 7, 1),
    (15, 9, 2);
