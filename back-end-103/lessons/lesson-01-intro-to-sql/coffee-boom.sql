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

