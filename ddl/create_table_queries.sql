-----------------------------------------------------------
-- 1. USERS TABLE
-----------------------------------------------------------
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) CHECK (role IN ('admin', 'staff')) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------------
-- 2. CATEGORIES
-----------------------------------------------------------
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-----------------------------------------------------------
-- 3. PRODUCTS
-----------------------------------------------------------
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(category_id) ON DELETE SET NULL,
    product_name VARCHAR(150) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    barcode VARCHAR(50),
    unit VARCHAR(20),  -- pcs, kg, litre, etc.
    description TEXT,
    min_stock_level INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category_id);

-----------------------------------------------------------
-- 4. SUPPLIERS
-----------------------------------------------------------
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(150),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    gst_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------------
-- 5. PURCHASE ORDERS (STOCK-IN)
-----------------------------------------------------------
CREATE TABLE purchase_orders (
    purchase_id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(supplier_id) ON DELETE SET NULL,
    invoice_number VARCHAR(100),
    purchase_date DATE NOT NULL,
    total_amount NUMERIC(10,2) DEFAULT 0,
    tax_amount NUMERIC(10,2) DEFAULT 0,
    discount_amount NUMERIC(10,2) DEFAULT 0,
    final_amount NUMERIC(10,2) DEFAULT 0,
    created_by INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------------
-- 6. PURCHASE ITEMS
-----------------------------------------------------------
CREATE TABLE purchase_items (
    purchase_item_id SERIAL PRIMARY KEY,
    purchase_id INT REFERENCES purchase_orders(purchase_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity INT NOT NULL,
    cost_price NUMERIC(10,2) NOT NULL,
    selling_price NUMERIC(10,2) NOT NULL,
    tax_percent NUMERIC(5,2),
    total_price NUMERIC(10,2) NOT NULL
);

CREATE INDEX idx_purchase_items_pid ON purchase_items(purchase_id);

-----------------------------------------------------------
-- 7. INVENTORY
-----------------------------------------------------------
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT UNIQUE REFERENCES products(product_id) ON DELETE CASCADE,
    quantity_available INT DEFAULT 0,
    last_restock_date DATE,
    last_updated TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------------
-- 8. CUSTOMERS
-----------------------------------------------------------
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

DROP TABLE sales_items;

-----------------------------------------------------------
-- 9. SALES (BILLING)
-----------------------------------------------------------
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    customer_id INT REFERENCES customers(customer_id) ON DELETE SET NULL,
    sale_date TIMESTAMP DEFAULT NOW(),
    total_quantity INT DEFAULT 0,
    total_amount NUMERIC(10,2) DEFAULT 0,
    discount_amount NUMERIC(10,2) DEFAULT 0,
    tax_amount NUMERIC(10,2) DEFAULT 0,
    final_amount NUMERIC(10,2) DEFAULT 0,
    payment_mode VARCHAR(20) CHECK (payment_mode IN ('cash', 'card', 'upi', 'bank')),
    created_by INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------------
-- 10. SALES ITEMS
-----------------------------------------------------------
CREATE TABLE sales_items (
    sales_item_id SERIAL PRIMARY KEY,
    sale_id INT REFERENCES sales(sale_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    selling_price NUMERIC(10,2) NOT NULL,
    discount_pct NUMERIC(10, 2) DEFAULT 5.0,
    tax_percent NUMERIC(5,2),
    total_price NUMERIC(10,2) NOT NULL
);

CREATE INDEX idx_sales_items_sid ON sales_items(sale_id);

-----------------------------------------------------------
-- 10.1 PROMOTION TABLE
-----------------------------------------------------------
CREATE TABLE promotion_discount (
	promotion_id SERIAL PRIMARY KEY,
	product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
	discount NUMERIC(5, 2) DEFAULT 0.05,
	promotion_name TEXT,
	start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE NOT NULL DEFAULT (CURRENT_DATE + INTERVAL '30 DAY'),
    created_at TIMESTAMP DEFAULT NOW()
)

-----------------------------------------------------------
-- 11. SALES RETURNS
-----------------------------------------------------------
CREATE TABLE sales_returns (
    return_id SERIAL PRIMARY KEY,
    sale_id INT REFERENCES sales(sale_id) ON DELETE CASCADE,
    return_date DATE NOT NULL,
    reason TEXT,
    refunded_amount NUMERIC(10,2) DEFAULT 0
);

-----------------------------------------------------------
-- 12. SALES RETURN ITEMS
-----------------------------------------------------------
CREATE TABLE sales_return_items (
    return_item_id SERIAL PRIMARY KEY,
    return_id INT REFERENCES sales_returns(return_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    refund_amount NUMERIC(10,2) NOT NULL
);

-----------------------------------------------------------
-- 13. TAX TABLE
-----------------------------------------------------------
CREATE TABLE tax_rates (
    tax_id SERIAL PRIMARY KEY,
    tax_name VARCHAR(50),
    tax_percent NUMERIC(5,2)
);


DROP TABLE payment_transactions CASCADE;

-----------------------------------------------------------
-- 14. PAYMENT TRANSACTIONS
-----------------------------------------------------------
CREATE TABLE payment_transactions (
    transaction_id SERIAL PRIMARY KEY,
    sale_id INT REFERENCES sales(sale_id) ON DELETE CASCADE,
    amount_paid NUMERIC(10,2),
    payment_mode VARCHAR(20) NOT NULL CHECK (payment_mode in ('cash', 'card', 'upi', 'bank')),
    payment_status  VARCHAR(20) DEFAULT 'SUCCESS' CHECK (payment_status in ('SUCCESS', 'FAILED', 'PENDING')),
    reference_number VARCHAR(100),
    payment_date TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------------
-- 15. AUDIT LOGS
-----------------------------------------------------------
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    action TEXT,
    table_name VARCHAR(50),
    record_id INT,
    old_data JSONB,
    new_data JSONB,
    action_date TIMESTAMP DEFAULT NOW()
);
