INSERT INTO users (username, password_hash, full_name, role, is_active)
VALUES
('admin01', 'hashed_admin_pass', 'Harendra Kumar', 'admin', TRUE),
('staff01', 'hashed_staff1_pass', 'Ravi Sharma', 'staff', TRUE),
('staff02', 'hashed_staff2_pass', 'Pooja Verma', 'staff', TRUE),
('staff03', 'hashed_staff3_pass', 'Amit Singh', 'staff', TRUE),
('staff04', 'hashed_staff4_pass', 'Neha Patel', 'staff', TRUE);

INSERT INTO categories (name, description)
VALUES
('Beverages', 'Soft drinks, juices, water'),
('Snacks', 'Chips, biscuits, namkeen'),
('Dairy', 'Milk, curd, cheese, butter'),
('Groceries', 'Daily essentials and staples'),
('Personal Care', 'Soaps, shampoos, toothpaste');


INSERT INTO products (category_id, product_name, sku, barcode, unit, description, min_stock_level)
VALUES
(1, 'Coca Cola 1L',       'BEV-COCO-1L', '8901234567891', 'bottle', '1 litre soft drink', 10),
(1, 'Bisleri Water 1L',   'BEV-BISL-1L', '8901234567892', 'bottle', 'Packaged drinking water', 20),
(2, 'Lays Chips - Classic Salted', 'SNK-LAYS-CLS', '8901234567893', 'packet', 'Potato chips', 15),
(3, 'Amul Butter 100g',   'DRY-AMUL-BUT', '8901234567894', 'pack', 'Salted butter', 8),
(4, 'India Gate Basmati Rice 5kg', 'GRC-RICE-5KG', '8901234567895', 'bag', '5kg premium basmati rice', 5);



INSERT INTO suppliers (supplier_name, contact_name, phone, email, address)
VALUES
('Hindustan Beverages Ltd', 'Sanjay Mehta', '9876543210', 'sales@hbl.com', 'Mumbai, Maharashtra'),
('FreshSnacks Distributors', 'Rohit Gupta', '9988776655', 'contact@fsd.com', 'Delhi'),
('Amul Dairy Suppliers', 'Kiran Patel', '9123456780', 'support@amul.com', 'Anand, Gujarat'),
('GroceryMart Wholesale', 'Aakash Jain', '9080706050', 'info@gmart.com', 'Jaipur'),
('Personal Care Hub', 'Swati Nair', '9090909090', 'help@pchub.com', 'Bengaluru');

INSERT INTO inventory (product_id, quantity_available, last_restock_date)
VALUES
    (1, 120, '2025-01-10'),  -- Amul Milk 1L
    (2, 45,  '2025-01-08'),  -- Fortune Sunflower Oil 1L
    (3, 320, '2025-01-12'),  -- Aashirvaad Atta 10kg
    (4, 85,  '2025-01-05'),  -- Parle-G Biscuit 80g
    (5, 60,  '2025-01-11');  -- Colgate Toothpaste 150g
    
 
INSERT INTO customers (full_name, phone, email, address) VALUES
('Rahul Sharma', '9876543210', 'rahul.sharma@example.com', '12/5 MG Road, Bengaluru, Karnataka'),
('Priya Nair', '9988776655', 'priya.nair@example.com', 'Flat 203, Green Valley Apartments, Kochi, Kerala'),
('Abhishek Verma', '9123456780', 'abhishek.verma@example.com', 'Sector 21, Noida, Uttar Pradesh'),
('Sneha Kulkarni', '9845098450', 'sneha.kulkarni@example.com', 'Shivajinagar, Pune, Maharashtra'),
('Mohammed Irfan', '9000012345', 'irfan.mhd@example.com', 'Old City, Hyderabad, Telangana');


SELECT * from inventory;

DROP TABLE inventory;

INSERT INTO inventory (product_id, quantity_available, last_restock_date)
VALUES
-- 1. Butter (product_id = 1)
(1, 120, '2025-01-20'),

-- 2. Parle-G Biscuit (product_id = 2)
(2, 450, '2025-01-18'),

-- 3. Fortune Sunflower Oil 1L (product_id = 3)
(3, 80, '2025-01-15'),

-- 4. Tata Salt 1kg (product_id = 4)
(4, 300, '2025-01-10'),

-- 5. Colgate Toothpaste 100g (product_id = 5)
(5, 200, '2025-01-22');



SELECT * FROM customers;

SELECT * FROM sales;

SELECT * FROM sales_items;

SELECT * from purchase_items;

SELECT * from products;

SELECT * from inventory;

select * from categories;

delete from categories
WHERE category_id in (6, 8, 9)

SELECT * from payment_transactions;

UPDATE products
SET description='1 litre Orange juice tetrapack'
where product_id=6;

UPDATE categories
SET category_id=6
WHERE category_id=7;

ALTER TABLE inventory
ADD COLUMN reorder_level INT DEFAULT 15 NOT NULL;

SELECT * FROM inventory;

UPDATE inventory
SET quantity_available=21
WHERE inventory_id=2 and product_id=2;

UPDATE inventory
SET quantity_available=18
WHERE inventory_id=3;

UPDATE inventory
SET quantity_available=17
WHERE inventory_id=1;