
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
  "user_type" TEXT NOT NULL CHECK("user_type" IN ('admin', 'user'))
);

-- Index on username
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
  "password" VARCHAR(45) NOT NULL,
  "bank_name" VARCHAR(45) NULL,
  "account_number" VARCHAR(45) NULL,
  "branch_code" VARCHAR(45) NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index on name
CREATE INDEX IF NOT EXISTS "idx_vendor_name" ON "vendor" ("name");

-----------------------------------------------------
-- Table "menuItem"
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "menuItem" (
  "menuItem_id" INTEGER PRIMARY KEY,
  "vendor_id" INT NOT NULL,
  "catagory" VARCHAR(45) NOT NULL,
  "name" VARCHAR(45) NOT NULL,
  "price" NUMERIC(10,2) NOT NULL,
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "cost" NUMERIC(10,2) NOT NULL,
  CONSTRAINT "fk_menuItem_vendor1"
    FOREIGN KEY ("vendor_id")
    REFERENCES "vendor" ("vendor_id")
);

-- Index on vendor_id
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

-- Index on user_id
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
-- Triggers for "updated_at"
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
-- Insert Dummy Data
-----------------------------------------------------
-- DUMMY DATA FOR TESTING

-- 1. Insert  "user"
INSERT INTO "user" ("user_id", "username", "password", "student_number", "name", "surname", "date_of_birth", "cell_number", "email", "user_type") VALUES
(1, 'willemk100', 'p@ssword1', 'u04868260', 'Willem', 'Kleynhans', '2004-03-17', '0812345678', 'willem@uni.com', 'admin'),
(2, 'jessM100', 'p@ssword2', 'u23232323', 'Jessica', 'Muller', '2000-11-20', '0729876543', 'jess@uni.com', 'user');

-- 2. Insert  "vendor"
INSERT INTO "vendor" ("vendor_id", "name", "location", "phone_number", "email", "password", "bank_name", "account_number", "branch_code") VALUES
(101, 'Tenz', 'University of Pretoria, Akanyang Building, 68 Lunnon Rd, Hatfield, Pretoria, 0028', '0662230306', 'tenz@up.com', 'tenzpassword', 'FNB', '62112233445', '250655');

-- 3. Insert  "menuItem"
INSERT INTO "menuItem" ("menuItem_id", "vendor_id", "catagory", "name", "price", "cost") VALUES
(1001, 101, 'Tramezini', 'Cheese & Tomato', 43.90, 25.00),
(1002, 101, 'Tramezini', 'Bacon & Cheese', 51.90, 26.90),
(1003, 101, 'Wrap', 'Tika Chicken Roti', 52.90, 30.00),
(1004, 101, 'Wrap', 'Hallomi & Mediteranean', 52.90, 30.00),
(1005, 101, 'Classic Shakes', 'Lime', 32.50, 15.00),
(1006, 101, 'Classic Shakes', 'Chocolate', 32.50, 15.00);
(1007, 101, 'Tramezini', 'Bacon & Avo', 59.90, 32.90),
(1008, 101, 'Tramezini', 'Rib & Mozzerella', 63.90, 26.90),
(1009, 101, 'Tramezini', 'Chicken, Bacon & Cheese', 59.90, 39.90),
(1010, 101, 'Burgers', 'Beef', 34.90, 26.90),
(1011, 101, 'Burgers', 'Chicken', 34.90, 26.90),
(1012, 101, 'Burgers', 'Rib', 34.90, 26.90);

-- 4. Insert into "order"
INSERT INTO "order" ("order_id", "user_id", "status") VALUES
(1001, 2, 'Collected'), 
(1002, 2, 'Submitted');

-- 5. Insert into "orderItem" 
INSERT INTO "orderItem" ("order_order_id", "menuItem_menuItem_id", "quantity", "price_per_item") VALUES
(1001, 1001, 1, 43.90),
(1001, 1005, 2, 32.50),
(1002, 1003, 1, 52.90);

