
-- Enable foreign key constraints (important for integrity)
PRAGMA foreign_keys = ON;

-----------------------------------------------------
-- Table "user"
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "user" (
  "user_id" INTEGER PRIMARY KEY,
  "username" VARCHAR(45) NOT NULL,
  "password" VARCHAR(45) NOT NULL,
  "student_number" VARCHAR(45) NULL,
  "name" VARCHAR(45) NOT NULL,
  "surname" VARCHAR(45) NOT NULL,
  "date_of_birth" TEXT NOT NULL,
  "cell_number" VARCHAR(45) NOT NULL,
  "email" VARCHAR(45) NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "user_type" TEXT NOT NULL CHECK("user_type" IN ('admin', 'customer'))
);

-- Index on username (AK)
CREATE UNIQUE INDEX IF NOT EXISTS "idx_user_username" ON "user" ("username");

-----------------------------------------------------
-- Table "vendor"
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "vendor" (
  "vendor_id" INTEGER PRIMARY KEY,
  "name" VARCHAR(45) NOT NULL,
  "location" VARCHAR(90) NOT NULL,
  "phone_number" VARCHAR(10) NOT NULL,
  "email" VARCHAR(90) NOT NULL,
  "username" VARCHAR(45) NOT NULL,
  "password" VARCHAR(45) NOT NULL,
  "bank_name" VARCHAR(45) NULL,
  "account_number" VARCHAR(45) NULL,
  "branch_code" VARCHAR(45) NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index on name (FK)
CREATE INDEX IF NOT EXISTS "idx_vendor_name" ON "vendor" ("name");

-----------------------------------------------------
-- Table "menuItem"
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "menuItem" (
  "menuItem_id" INTEGER PRIMARY KEY,
  "vendor_id" INT NOT NULL,
  "category" VARCHAR(45) NOT NULL,
  "name" VARCHAR(45) NOT NULL,
  "price" NUMERIC(10,2) NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "cost" NUMERIC(10,2) NOT NULL,
  CONSTRAINT "fk_menuItem_vendor1"
    FOREIGN KEY ("vendor_id")
    REFERENCES "vendor" ("vendor_id")
);

-- Index on vendor_id (FK)
CREATE INDEX IF NOT EXISTS "fk_menuItem_vendor1_idx" ON "menuItem" ("vendor_id");

-----------------------------------------------------
-- Table "order" 
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "order" (
  "order_id" INTEGER PRIMARY KEY,
  "user_id" INT NOT NULL,
  "order_date" TEXT NOT NULL DEFAULT (datetime('now')),
  "status" TEXT NOT NULL DEFAULT 'Submitted' CHECK("status" IN ('Submitted', 'Preparing', 'Ready', 'Collected', 'Not Collected')),
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  CONSTRAINT "fk_order_user1"
    FOREIGN KEY ("user_id")
    REFERENCES "user" ("user_id")
);

-- Index on user_id (FK
CREATE INDEX IF NOT EXISTS "fk_order_user1_idx" ON "order" ("user_id");

-----------------------------------------------------
-- Table "orderItem" 
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "orderItem" (
  "orderItem_id" INTEGER PRIMARY KEY,
  "order_order_id" INT NOT NULL,
  "menuItem_menuItem_id" INT NOT NULL,
  "quantity" INTEGER NOT NULL DEFAULT 1,
  "price_per_item" NUMERIC(10,2) NOT NULL,
  CONSTRAINT "fk_orderItem_order1"
    FOREIGN KEY ("order_order_id")
    REFERENCES "order" ("order_id"),
  CONSTRAINT "fk_orderItem_menuItem1"
    FOREIGN KEY ("menuItem_menuItem_id")
    REFERENCES "menuItem" ("menuItem_id")
);

-- Indexes for FKs
CREATE INDEX IF NOT EXISTS "fk_orderItem_order1_idx" ON "orderItem" ("order_order_id");
CREATE INDEX IF NOT EXISTS "fk_orderItem_menuItem1_idx" ON "orderItem" ("menuItem_menuItem_id");


-----------------------------------------------------
-- Triggers to make the updated_at field auto-update
-----------------------------------------------------

-- User Table Trigger
CREATE TRIGGER IF NOT EXISTS update_user_updated_at 
AFTER UPDATE ON "user"
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at 
BEGIN
    UPDATE "user" SET updated_at = datetime('now') WHERE user_id = NEW.user_id;
END;

-- Vendor Table Trigger
CREATE TRIGGER IF NOT EXISTS update_vendor_updated_at 
AFTER UPDATE ON "vendor"
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at 
BEGIN
    UPDATE "vendor" SET updated_at = datetime('now') WHERE vendor_id = NEW.vendor_id;
END;

-- MenuItem Table Trigger
CREATE TRIGGER IF NOT EXISTS update_menuitem_updated_at 
AFTER UPDATE ON "menuItem"
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at 
BEGIN
    UPDATE "menuItem" SET updated_at = datetime('now') WHERE menuItem_id = NEW.menuItem_id;
END;

-- Order Table Trigger
CREATE TRIGGER IF NOT EXISTS update_order_updated_at 
AFTER UPDATE ON "order"
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at 
BEGIN
    UPDATE "order" SET updated_at = datetime('now') WHERE order_id = NEW.order_id;
END;

-----------------------------------------------------
-- Example Data - Based on TENZ restaurant and its menu.
-----------------------------------------------------


-- 1. "user"
INSERT INTO "user" ("user_id", "username", "password", "student_number", "name", "surname", "date_of_birth", "cell_number", "email", "user_type") VALUES
(1, 'willemk100', 'p@ssword1', 'u04868260', 'Willem', 'Kleynhans', '2004-03-17', '0812345678', 'willem@uni.com', 'admin'),
(2, 'jessM100', 'p@ssword2', 'u23232323', 'Jessica', 'Muller', '2000-11-20', '0729876543', 'jess@uni.com', 'customer'),
(3, 'jmk200', 'p@ssword3', 'u01234566', 'Ayden', 'Bouwer', '2004-09-17', '081234567', 'AydenB@uni.com', 'customer')
-- (4, 'EthanR789', 'qW9eRt2Y', 'u39458210', 'Ethan', 'Ross', '1967-05-12', '0821098765', 'EthanR@uni.com', 'admin'),
-- (5, 'SophiaA321', 'zX3cVb1N', 'u50129347', 'Sophia', 'Adams', '2001-09-25', '0734561234', 'SophiaA@uni.com', 'user'),
-- (6, 'OwenM456', 'pL7kJh4G', 'u61870529', 'Owen', 'Miller', '1985-02-08', '0649873210', 'OwenM@uni.com', 'vendor'),
-- (7, 'ChloeW111', 'dF5gHj8K', 'u72541638', 'Chloe', 'Wilson', '2003-11-04', '0836549870', 'ChloeW@uni.com', 'user'),
-- (8, 'LiamB222', 'aS1dQw0E', 'u83212746', 'Liam', 'Baker', '1974-07-19', '0715432109', 'LiamB@uni.com', 'admin'),
-- (9, 'IslaG333', 'tY6uIo9P', 'u94983855', 'Isla', 'Green', '1992-03-30', '0847654321', 'IslaG@uni.com', 'vendor'),
-- (10, 'NoahJ444', 'mN4bVc7X', 'u05654964', 'Noah', 'Jones', '2006-01-15', '0601239876', 'NoahJ@uni.com', 'user'),
-- (11, 'AvaS555', 'kL8jUz5W', 'u16325073', 'Ava', 'Scott', '1960-10-01', '0798765432', 'AvaS@uni.com', 'admin'),
-- (12, 'JamesC666', 'rT0yUi3O', 'u27096182', 'James', 'Clark', '1988-06-22', '0823456789', 'JamesC@uni.com', 'vendor'),
-- (13, 'MiaP777', 'hG2fDs6A', 'u38767291', 'Mia', 'Parker', '2000-04-11', '0617654321', 'MiaP@uni.com', 'user'),
-- (14, 'LucasF888', 'bV9cNx4M', 'u49438300', 'Lucas', 'Foster', '1970-12-05', '0742109876', 'LucasF@uni.com', 'admin'),
-- (15, 'EvelynD999', 'wQ5eRz8T', 'u50109419', 'Evelyn', 'Davis', '1995-08-14', '0815436789', 'EvelynD@uni.com', 'vendor'),
-- (16, 'BenjaminK10', 'iO2pUj7Y', 'u61780528', 'Benjamin', 'King', '2004-02-07', '0728761234', 'BenjaminK@uni.com', 'user'),
-- (17, 'AmeliaL20', 'fD4sWe1Q', 'u72451637', 'Amelia', 'Lee', '1963-09-28', '0834560123', 'AmeliaL@uni.com', 'admin'),
-- (18, 'MasonH30', 'gH6jKl9Z', 'u83122746', 'Mason', 'Hall', '1981-04-20', '0605432109', 'MasonH@uni.com', 'vendor'),
-- (19, 'HarperT40', 'cM3nVb5X', 'u94893855', 'Harper', 'Turner', '1998-12-18', '0791098765', 'HarperT@uni.com', 'user'),
-- (20, 'ElijahV50', 'lK7jHg0F', 'u05564964', 'Elijah', 'Vance', '1978-01-26', '0843210987', 'ElijahV@uni.com', 'admin'),
-- (21, 'AbigailR60', 'pO1iUy6T', 'u16235073', 'Abigail', 'Reid', '1990-11-02', '0628765432', 'AbigailR@uni.com', 'vendor'),
-- (22, 'LoganZ70', 'eW8qAz3S', 'u27906182', 'Logan', 'Zimmerman', '2005-08-01', '0736549876', 'LoganZ@uni.com', 'user'),
-- (23, 'EllaE80', 'rF4gDj1H', 'u38677291', 'Ella', 'Evans', '1966-03-17', '0812340567', 'EllaE@uni.com', 'admin'),
-- (24, 'AidenN90', 'vB6nCm2K', 'u49348300', 'Aiden', 'Nguyen', '1997-01-09', '0745678901', 'AidenN@uni.com', 'vendor'),
-- (25, 'ScarlettH00', 'yU9iOj5L', 'u50019419', 'Scarlett', 'Harris', '2002-07-29', '0829876540', 'ScarlettH@uni.com', 'user'),
-- (26, 'GabrielP11', 'zX1cQb7W', 'u61690528', 'Gabriel', 'Peterson', '1972-10-14', '0641234567', 'GabrielP@uni.com', 'admin'),
-- (27, 'LaylaT22', 'sA3dFp0O', 'u72361637', 'Layla', 'Thompson', '1984-05-23', '0795432108', 'LaylaT@uni.com', 'vendor'),
-- (28, 'JacksonC33', 'hJ8kLz4X', 'u83032746', 'Jackson', 'Chen', '1999-06-10', '0837654329', 'JacksonC@uni.com', 'user'),
-- (29, 'ZoeyM44', 'bN5mCv6Z', 'u94703855', 'Zoey', 'Morales', '1969-11-20', '0602109876', 'ZoeyM@uni.com', 'admin'),
-- (30, 'CalebS55', 'qE9wRt2Y', 'u05374964', 'Caleb', 'Shah', '1993-02-16', '0714321098', 'CalebS@uni.com', 'vendor'),
-- (31, 'HazelB66', 'tI0oPu3R', 'u16045073', 'Hazel', 'Bailey', '2003-03-05', '0846543210', 'HazelB@uni.com', 'user'),
-- (32, 'JulianK77', 'aD7fGh1J', 'u27716182', 'Julian', 'Kaur', '1976-08-09', '0621098765', 'JulianK@uni.com', 'admin'),
-- (33, 'StellaW88', 'mX4zCv8B', 'u38387291', 'Stella', 'White', '1986-12-28', '0733210987', 'StellaW@uni.com', 'vendor'),
-- (34, 'LeoD99', 'lP5oKj9H', 'u49058300', 'Leo', 'Dubois', '2001-05-14', '0815432109', 'LeoD@uni.com', 'user'),
-- (35, 'VioletF12', 'wS2qEr4T', 'u50729419', 'Violet', 'Fisher', '1961-07-03', '0748765432', 'VioletF@uni.com', 'admin'),
-- (36, 'HenryL34', 'rY8uIo6P', 'u61390528', 'Henry', 'Liu', '1996-04-29', '0820123456', 'HenryL@uni.com', 'vendor'),
-- (37, 'AriaM56', 'xZ3cAs1D', 'u72061637', 'Aria', 'Mendez', '2004-11-21', '0616543219', 'AriaM@uni.com', 'user'),
-- (38, 'DanielR78', 'kG6jHl7F', 'u82732746', 'Daniel', 'Russo', '1979-01-11', '0799876540', 'DanielR@uni.com', 'admin'),
-- (39, 'SkylarP90', 'vC9bNm5X', 'u93403855', 'Skylar', 'Patel', '1989-10-06', '0831234567', 'SkylarP@uni.com', 'vendor'),
-- (40, 'RyanG01', 'jH1kLp0O', 'u04074964', 'Ryan', 'Grant', '2000-08-27', '0604321098', 'RyanG@uni.com', 'user'),
-- (41, 'GraceB23', 'qA4zXw7E', 'u15745073', 'Grace', 'Brooks', '1973-05-02', '0716543210', 'GraceB@uni.com', 'admin'),
-- (42, 'MaxW45', 'tD9fSg2H', 'u26416182', 'Max', 'Wagner', '1991-03-13', '0848765431', 'MaxW45@uni.com', 'vendor'),
-- (43, 'LunaC67', 'iO5pUj8Y', 'u37087291', 'Luna', 'Cooper', '2005-09-03', '0623456780', 'LunaC@uni.com', 'user'),
-- (44, 'VictorS89', 'fG7hJk3L', 'u48758300', 'Victor', 'Smith', '1965-06-24', '0739012345', 'VictorS@uni.com', 'admin'),
-- (45, 'ElenaK01', 'nM0bVc5Z', 'u59429419', 'Elena', 'Keller', '1994-12-19', '0817890123', 'ElenaK@uni.com', 'vendor'),
-- (46, 'MilesA23', 'rT6yUi2O', 'u60090528', 'Miles', 'Allen', '1998-01-20', '0740123456', 'MilesA@uni.com', 'user'),
-- (47, 'PhoebeL45', 'dA8sQz9W', 'u71761637', 'Phoebe', 'Lopez', '1977-11-08', '0825678901', 'PhoebeL@uni.com', 'admin'),
-- (48, 'SamN67', 'hJ4kLp1Z', 'u82432746', 'Sam', 'Nelson', '1983-09-26', '0619876543', 'SamN67@uni.com', 'vendor'),
-- (49, 'RubyD89', 'cM5nBv0X', 'u93103855', 'Ruby', 'Dixon', '2002-10-16', '0793456789', 'RubyD@uni.com', 'user'),
-- (50, 'WesleyE01', 'lK9jHg2F', 'u04774964', 'Wesley', 'Edwards', '1968-04-18', '0846789012', 'WesleyE@uni.com', 'admin'),
-- (51, 'ZaraS23', 'pO3iUy4T', 'u15445073', 'Zara', 'Stone', '1990-06-07', '0621234567', 'ZaraS23@uni.com', 'vendor'),
-- (52, 'DeanH45', 'eW5qAr6S', 'u26116182', 'Dean', 'Hayes', '2006-03-01', '0734567890', 'DeanH45@uni.com', 'user'),
-- (53, 'NicoleV67', 'rF0gDj7H', 'u37787291', 'Nicole', 'Vega', '1970-02-14', '0818901234', 'NicoleV67@uni.com', 'admin')
;

-- 2. "vendor"
INSERT INTO "vendor" ("vendor_id", "name", "location", "phone_number", "email", "username", "password", "bank_name", "account_number", "branch_code") VALUES
(101, 'Tenz', 'University of Pretoria, Akanyang Building, 68 Lunnon Rd, Hatfield, Pretoria, 0028', '0662230306', 'tenz@up.com', 'tenzusername', 'tenzpassword', 'FNB', '62112233445', '250655');

-- 3. "menuItem"
INSERT INTO "menuItem" ("menuItem_id", "vendor_id", "category", "name", "price", "cost") VALUES
(1001, 101, 'Tramezini', 'Cheese & Tomato', 43.90, 25.00),
(1002, 101, 'Tramezini', 'Bacon & Cheese', 51.90, 26.90),
(1003, 101, 'Wrap', 'Tika Chicken Roti', 52.90, 30.00),
(1004, 101, 'Wrap', 'Hallomi & Mediteranean', 52.90, 30.00),
(1005, 101, 'Classic Shakes', 'Lime', 32.50, 15.00),
(1006, 101, 'Classic Shakes', 'Chocolate', 32.50, 15.00),
(1007, 101, 'Tramezini', 'Bacon & Avo', 59.90, 32.90),
(1008, 101, 'Tramezini', 'Rib & Mozzerella', 63.90, 26.90),
(1009, 101, 'Tramezini', 'Chicken, Bacon & Cheese', 59.90, 39.90),
(1010, 101, 'Burgers', 'Beef', 34.90, 26.90),
(1011, 101, 'Burgers', 'Chicken', 34.90, 26.90),
(1012, 101, 'Burgers', 'Rib', 34.90, 26.90)
(1013, 101, 'Fries', 'Small', 15.00, 10.00),
(1014, 101, 'Fries', 'Medium', 20.00, 12.00),
(1015, 101, 'Fries', 'Large', 25.00, 15.00);

-- 4. "order"
INSERT INTO "order" ("order_id", "user_id", "status") VALUES
(1001, 2, 'Collected'), 
(1002, 2, 'Submitted');

-- 5. "orderItem" 
INSERT INTO "orderItem" ("order_order_id", "menuItem_menuItem_id", "quantity", "price_per_item") VALUES
(1001, 1001, 1, 43.90),
(1001, 1005, 2, 32.50),
(1002, 1003, 1, 52.90);

