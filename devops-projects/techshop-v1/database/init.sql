-- Добавление данных в таблицы
INSERT INTO categories (name, description) VALUES
('Notebooks', 'Portable computers for work and entertainment.'),
('Smartphones', 'Mobile devices with advanced features and connectivity.'),
('Headphones', 'Audio devices for personal listening.'),
('Cameras', 'Devices for capturing photos and videos.'),
('Gaming Consoles', 'Devices for playing video games.'),
('Smartwatches', 'Wearable devices with smart features.'),
('Tablets', 'Touchscreen devices for browsing and media consumption.'),
('Printers', 'Devices for producing physical copies of documents and images.'),
('Monitors', 'Display screens for computers and entertainment.'),
('Keyboards', 'Input devices for typing and gaming.');

-- Добавление товаров в таблицу products
INSERT INTO products (name, description, price, stock, category_id) VALUES
('MacBook Pro 13"', 'Apple M1 chip, 8GB RAM, 256GB SSD', 1299.99, 10, 1),
('iPhone 11', 'A13 Bionic chip, 4GB RAM, 64GB storage', 699.99, 5, 2),
('Samsung Galaxy S20', 'Exynos 9820 chip, 8GB RAM, 128GB storage', 899.99, 7, 2),
('Sony WH-1000XM4', 'Noise-canceling wireless headphones', 349.99, 15, 3),
('Canon EOS R5', '45MP full-frame mirrorless camera', 3899.99, 3, 4),
('PlayStation 5', 'Next-gen gaming console with ultra-fast SSD', 499.99, 20, 5),
('Apple Watch Series 6', 'GPS + Cellular, Blood Oxygen app', 399.99, 8, 6),
('iPad Pro 11"', 'Apple M1 chip, 8GB RAM, 128GB storage', 799.99, 12, 7),
('HP LaserJet Pro M404n', 'Monochrome laser printer with fast printing speed', 299.99, 10, 8),
('Dell UltraSharp U2720Q', '27-inch 4K monitor with USB-C connectivity', 599.99, 5, 9),
('Logitech MX Keys', 'Wireless keyboard with smart illumination', 99.99, 25, 10),
('Asus ROG Strix G15', 'Gaming laptop with AMD Ryzen 9 and NVIDIA RTX 3070', 1499.99, 4, 1),
('Google Pixel 5', 'Snapdragon 765G chip, 8GB RAM, 128GB storage', 699.99, 6, 2),
('Bose QuietComfort 35 II', 'Wireless Bluetooth headphones with noise cancellation', 299.99, 10, 3),
('Nikon Z6 II', '24.5MP full-frame mirrorless camera', 1999.99, 2, 4),
('Xbox Series X', 'Powerful gaming console with fast load times', 499.99, 15, 5),
('Samsung Galaxy Watch Active2', 'Fitness-focused smartwatch with heart rate monitoring', 249.99, 10, 6),
('Microsoft Surface Pro 7', '2-in-1 laptop with touchscreen and detachable keyboard', 899.99, 7, 7),
('Canon PIXMA TS9120', 'All-in-one inkjet printer with wireless connectivity', 199.99, 12, 8),
('LG UltraFine 27MD5KL-B', '27-inch 5K monitor designed for Mac users', 1299.99, 3, 9),
('Razer BlackWidow Elite', 'Mechanical gaming keyboard with customizable RGB lighting', 169.99, 20, 10);

-- Добавление заказов и элементов заказа в таблицы orders и order_items
INSERT INTO orders (user_name, user_email, total_price, status) VALUES
('John Doe', 'johndoe@example.com', 3099.97, 'pending'),
('Jane Smith', 'janesmith@example.com', 1049.98, 'shipped'),
('Bob Johnson', 'bobjohnson@example.com', 4399.98, 'delivered'),
('Alice Williams', 'alicewilliams@example.com', 1199.98, 'cancelled'),
('Charlie Brown', 'charliebrown@example.com', 2499.96, 'pending');

-- Добавление элементов заказа для каждого заказа в таблицу order_items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1299.99),
(1, 3, 2, 1799.98),
(2, 2, 1, 699.99),
(2, 4, 1, 349.99),
(3, 5, 1, 3899.99),
(3, 6, 1, 499.99),
(4, 7, 1, 399.99),
(4, 8, 1, 799.99),
(5, 9, 1, 299.99),
(5, 10, 1, 599.99),
(5, 11, 1, 99.99),
(5, 12, 1, 1499.99),