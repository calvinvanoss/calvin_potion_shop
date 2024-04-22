DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS potions;
DROP TABLE IF EXISTS global_inventory;

CREATE TABLE global_inventory (
    id INT PRIMARY KEY,
    red_ml INT NOT NULL,
    green_ml INT NOT NULL,
    blue_ml INT NOT NULL,
    gold INT NOT NULL
);

CREATE TABLE potions (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    potion_type INT[] NOT NULL
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

INSERT INTO global_inventory (id, red_ml, green_ml, blue_ml, gold)
VALUES (1, 0, 0, 0, 100);
INSERT INTO potions (sku, name, quantity, price, potion_type)
VALUES ('RED_POTION_0', 'red potion', 0, 50, ARRAY[100, 0, 0, 0]),
       ('GREEN_POTION_0', 'green potion', 0, 50, ARRAY[0, 100, 0, 0]),
       ('BLUE_POTION_0', 'blue potion', 0, 50, ARRAY[0, 0, 100, 0]),
       ('YELLOW_POTION_0', 'yellow potion', 0, 50, ARRAY[50, 50, 0, 0]),
       ('PURPLE_POTION_0', 'purple potion', 0, 50, ARRAY[50, 0, 50, 0]),
       ('CYAN_POTION_0', 'cyan potion', 0, 50, ARRAY[0, 50, 50, 0]);
