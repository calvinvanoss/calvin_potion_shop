DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS potion_ledger_entries;
DROP TABLE IF EXISTS potion_transactions;
DROP TABLE IF EXISTS potions;
DROP TABLE IF EXISTS global_inventory;

CREATE TABLE global_inventory (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    red_ml INT NOT NULL,
    green_ml INT NOT NULL,
    blue_ml INT NOT NULL,
    gold INT NOT NULL,
    description TEXT
);

CREATE TABLE potions (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price INT NOT NULL,
    potion_type INT[] NOT NULL
);

CREATE TABLE potion_transactions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

CREATE TABLE potion_ledger_entries (
    id SERIAL PRIMARY KEY,
    sku TEXT NOT NULL,
    quantity INT NOT NULL,
    transaction INT NOT NULL,
    FOREIGN KEY (sku) REFERENCES potions(sku),
    FOREIGN KEY (transaction) REFERENCES potion_transactions(id)
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL
);

CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL,
    sku TEXT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (sku) REFERENCES potions(sku)
);

INSERT INTO global_inventory (red_ml, green_ml, blue_ml, gold, description)
VALUES (0, 0, 0, 100, 'Starting inventory');
INSERT INTO potions (sku, name, price, potion_type)
VALUES ('RED_POTION_0', 'red potion', 50, ARRAY[100, 0, 0, 0]),
       ('GREEN_POTION_0', 'green potion', 50, ARRAY[0, 100, 0, 0]),
       ('BLUE_POTION_0', 'blue potion', 50, ARRAY[0, 0, 100, 0]),
       ('YELLOW_POTION_0', 'yellow potion', 50, ARRAY[50, 50, 0, 0]),
       ('PURPLE_POTION_0', 'purple potion', 50, ARRAY[50, 0, 50, 0]),
       ('CYAN_POTION_0', 'cyan potion', 50, ARRAY[0, 50, 50, 0]);
INSERT INTO potion_transactions (description)
VALUES ('Starting potion count');
INSERT INTO potion_ledger_entries (sku, quantity, transaction)
VALUES ('RED_POTION_0', 0, 1),
       ('GREEN_POTION_0', 0, 1),
       ('BLUE_POTION_0', 0, 1),
       ('YELLOW_POTION_0', 0, 1),
       ('PURPLE_POTION_0', 0, 1),
       ('CYAN_POTION_0', 0, 1);
