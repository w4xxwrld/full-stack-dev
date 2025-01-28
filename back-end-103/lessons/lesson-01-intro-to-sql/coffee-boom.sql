CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  product_name VARCHAR(50) NOT NULL,
  product_description TEXT NOT NULL,
  product_price DECIMAL(5, 2) NOT NULL,
  product_category VARCHAR(50) NOT NULL,
  product_status BOOLEAN NOT NULL,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(50) NOT NULL,
  customer_surname VARCHAR(50) NOT NULL,
  customer_email VARCHAR(50) NOT NULL,
  customer_phone VARCHAR(50) NOT NULL,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  bonus_points INT DEFAULT 0
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  order_sum FLOAT NOT NULL,
  order_status BOOLEAN NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  payment_method VARCHAR(50) NOT NULL
);

CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  product_id INT NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id),
  product_quantity INT NOT NULL,
  product_price DECIMAL(11, 2) NOT NULL
);

INSERT INTO products (product_name, product_description, product_price, product_category, product_status)
VALUES 
('Espresso', 'Strong and black coffee', 2.50, 'Beverage', TRUE),
('Latte', 'Coffee with steamed milk', 3.50, 'Beverage', TRUE),
('Cappuccino', 'Coffee with steamed milk foam', 3.00, 'Beverage', TRUE);

INSERT INTO customers (customer_name, customer_surname, customer_email, customer_phone)
VALUES 
('John', 'Doe', 'john.doe@example.com', '123-456-7890'),
('Jane', 'Smith', 'jane.smith@example.com', '098-765-4321');

INSERT INTO orders (customer_id, order_sum, order_status, payment_method)
VALUES 
(1, 6.00, TRUE, 'Credit Card');

INSERT INTO order_items (order_id, product_id, product_quantity, product_price)
VALUES 
(1, 1, 1, 2.50),
(1, 2, 1, 3.50);