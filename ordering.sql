
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
-- Table "orders" 
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "orders" (
  "order_id" INTEGER PRIMARY KEY,
  "user_id" INT NOT NULL,
  "order_date" TEXT NOT NULL DEFAULT (date('now')),
  "collection_time" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'Submitted' CHECK("status" IN ('Submitted', 'Preparing', 'Ready', 'Collected', 'Not Collected')),
  "created_at" TEXT NOT NULL DEFAULT (datetime('now')),
  "updated_at" TEXT NOT NULL DEFAULT (datetime('now')),
  CONSTRAINT "fk_order_user1"
    FOREIGN KEY ("user_id")
    REFERENCES "user" ("user_id")
);

-- Index on user_id (FK
CREATE INDEX IF NOT EXISTS "fk_order_user1_idx" ON "orders" ("user_id");

-----------------------------------------------------
-- Table "orderItem" 
-----------------------------------------------------
CREATE TABLE IF NOT EXISTS "orderItem" (
  "orderItem_id" INTEGER PRIMARY KEY,
  "orders_order_id" INT NOT NULL,
  "menuItem_menuItem_id" INT NOT NULL,
  "vendor_id" INT NOT NULL,
  "price_per_item" NUMERIC(10,2) NOT NULL,
  CONSTRAINT "fk_orderItem_order1"
    FOREIGN KEY ("orders_order_id")
    REFERENCES "orders" ("order_id"),
  CONSTRAINT "fk_orderItem_menuItem1"
    FOREIGN KEY ("menuItem_menuItem_id")
    REFERENCES "menuItem" ("menuItem_id")
);

-- Indexes for FKs
CREATE INDEX IF NOT EXISTS "fk_orderItem_order1_idx" ON "orderItem" ("orders_order_id");
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

-- Orders Table Trigger
CREATE TRIGGER IF NOT EXISTS update_orders_updated_at 
AFTER UPDATE ON "orders"
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at 
BEGIN
    UPDATE "orders" SET updated_at = datetime('now') WHERE order_id = NEW.order_id;
END;

-----------------------------------------------------
-- Example Data - Based on TENZ restaurant and its menu.
-----------------------------------------------------


-- 1. "user"
INSERT INTO "user" ("user_id", "username", "password", "student_number", "name", "surname", "date_of_birth", "cell_number", "email", "user_type") VALUES
(1, 'willemk100', 'p@ssword1', 'u04868260', 'Willem', 'Kleynhans', '2004-03-17', '0812345678', 'willem@uni.com', 'admin'),
(2, 'jessM100', 'p@ssword2', 'u23232323', 'Jessica', 'Muller', '2000-11-20', '0729876543', 'jess@uni.com', 'customer'),
(3, 'jmk200', 'p@ssword3', 'u01234566', 'Ayden', 'Bouwer', '2004-09-17', '081234567', 'AydenB@uni.com', 'customer');

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
(1012, 101, 'Burgers', 'Rib', 34.90, 26.90),
(1013, 101, 'Fries', 'Small', 15.00, 10.00),
(1014, 101, 'Fries', 'Medium', 20.00, 12.00),
(1015, 101, 'Fries', 'Large', 25.00, 15.00);


-- 4. "orders"
INSERT INTO "orders" ("order_id", "user_id", "order_date", "collection_time", "status") VALUES
-- October 1
(1001,2,'2025-10-01','10:15','Collected'),
(1002,3,'2025-10-01','11:30','Collected'),
(1003,2,'2025-10-01','13:00','Collected'),
-- October 2
(1004,3,'2025-10-02','10:45','Collected'),
(1005,2,'2025-10-02','12:00','Collected'),
(1006,3,'2025-10-02','13:30','Collected'),
-- October 3
(1007,2,'2025-10-03','09:50','Collected'),
(1008,3,'2025-10-03','11:15','Collected'),
(1009,2,'2025-10-03','12:40','Collected'),
-- October 4
(1010,3,'2025-10-04','10:10','Collected'),
(1011,2,'2025-10-04','11:45','Collected'),
(1012,3,'2025-10-04','13:05','Collected'),
-- October 5
(1013,2,'2025-10-05','10:30','Collected'),
(1014,3,'2025-10-05','12:00','Collected'),
(1015,2,'2025-10-05','13:20','Collected'),
-- October 6
(1016,3,'2025-10-06','09:50','Collected'),
(1017,2,'2025-10-06','11:30','Collected'),
(1018,3,'2025-10-06','12:45','Collected'),
-- October 7
(1019,2,'2025-10-07','10:05','Collected'),
(1020,3,'2025-10-07','11:20','Collected'),
(1021,2,'2025-10-07','12:40','Collected'),
-- October 8
(1022,3,'2025-10-08','10:15','Collected'),
(1023,2,'2025-10-08','11:50','Collected'),
(1024,3,'2025-10-08','13:05','Collected'),
-- October 9
(1025,2,'2025-10-09','09:10','Collected'),
(1026,3,'2025-10-09','11:35','Collected'),
(1027,2,'2025-10-09','16:55','Collected'),
-- October 10
(1028,3,'2025-10-10','10:25','Collected'),
(1029,2,'2025-10-10','11:40','Collected'),
(1030,3,'2025-10-10','12:50','Collected'),
-- October 11
(1031,2,'2025-10-11','10:00','Collected'),
(1032,3,'2025-10-11','11:30','Collected'),
(1033,2,'2025-10-11','12:45','Collected'),
-- October 12
(1034,3,'2025-10-12','10:15','Collected'),
(1035,2,'2025-10-12','11:50','Collected'),
(1036,3,'2025-10-12','13:05','Collected'),
-- October 13
(1037,2,'2025-10-13','10:10','Collected'),
(1038,3,'2025-10-13','11:35','Collected'),
(1039,2,'2025-10-13','12:55','Collected'),
-- October 14
(1040,3,'2025-10-14','10:25','Collected'),
(1041,2,'2025-10-14','11:40','Collected'),
(1042,3,'2025-10-14','12:50','Collected'),
-- October 15
(1043,2,'2025-10-15','10:00','Collected'),
(1044,3,'2025-10-15','11:30','Collected'),
(1045,2,'2025-10-15','12:45','Collected'),
-- October 16
(1046,3,'2025-10-16','10:15','Collected'),
(1047,2,'2025-10-16','11:50','Collected'),
(1048,3,'2025-10-16','13:05','Collected'),
-- October 17
(1049,2,'2025-10-17','10:10','Collected'),
(1050,3,'2025-10-17','11:35','Collected'),
(1051,2,'2025-10-17','12:55','Collected'),
-- October 18
(1052,3,'2025-10-18','10:25','Collected'),
(1053,2,'2025-10-18','11:40','Collected'),
(1054,3,'2025-10-18','15:50','Collected'),
-- October 19
(1055,2,'2025-10-19','10:00','Collected'),
(1056,3,'2025-10-19','11:30','Collected'),
(1057,2,'2025-10-19','12:45','Collected'),
-- October 20
(1058,3,'2025-10-20','10:15','Collected'),
(1059,2,'2025-10-20','11:50','Collected'),
(1060,3,'2025-10-20','13:05','Collected'),
-- October 21
(1061,2,'2025-10-21','10:10','Collected'),
(1062,3,'2025-10-21','11:35','Collected'),
(1063,2,'2025-10-21','12:55','Collected'),
-- October 22
(1064,3,'2025-10-22','10:25','Collected'),
(1065,2,'2025-10-22','11:40','Collected'),
(1066,3,'2025-10-22','12:50','Collected'),
-- October 23
(1067,2,'2025-10-23','10:00','Collected'),
(1068,3,'2025-10-23','11:30','Collected'),
(1069,2,'2025-10-23','12:45','Collected'),
-- October 24
(1070,3,'2025-10-24','10:15','Collected'),
(1071,2,'2025-10-24','11:50','Collected'),
(1072,3,'2025-10-24','13:05','Collected'),
-- October 25
(1073,2,'2025-10-25','10:10','Collected'),
(1074,3,'2025-10-25','11:35','Collected'),
(1075,2,'2025-10-25','12:55','Collected'),
-- October 26
(1076,3,'2025-10-26','10:25','Collected'),
(1077,2,'2025-10-26','11:40','Collected'),
(1078,3,'2025-10-26','12:50','Collected'),
-- October 27
(1079,2,'2025-10-27','10:00','Collected'),
(1080,3,'2025-10-27','11:30','Collected'),
(1081,2,'2025-10-27','12:45','Collected'),
-- October 28
(1082,3,'2025-10-28','10:15','Collected'),
(1083,2,'2025-10-28','11:50','Collected'),
(1084,3,'2025-10-28','13:05','Collected'),
-- October 29
(1085,2,'2025-10-29','10:10','Collected'),
(1086,3,'2025-10-29','11:35','Collected'),
(1087,2,'2025-10-29','12:55','Collected'),
-- October 30
(1088,3,'2025-10-30','10:25','Collected'),
(1089,2,'2025-10-30','11:40','Collected'),
(1090,3,'2025-10-30','12:50','Collected'),
-- October 31
(1091,2,'2025-10-31','10:00','Collected'),
(1092,3,'2025-10-31','11:30','Collected'),
(1093,2,'2025-10-31','12:45','Collected'),
-- November 1–6 (all Collected)
(1094,2,'2025-11-01','10:15','Collected'),
(1095,3,'2025-11-01','11:30','Collected'),
(1096,2,'2025-11-02','12:00','Collected'),
(1097,3,'2025-11-02','13:15','Collected'),
(1098,2,'2025-11-03','10:45','Collected'),
(1099,3,'2025-11-03','12:30','Collected'),
(1100,2,'2025-11-04','11:00','Collected'),
(1101,3,'2025-11-04','13:00','Collected'),
(1102,2,'2025-11-05','10:30','Collected'),
(1103,3,'2025-11-05','12:15','Collected'),
(1104,2,'2025-11-06','11:45','Collected'),
(1105,3,'2025-11-06','13:30','Collected'),
-- November 7 (today) → mix
(1106,2,'2025-11-07','10:15','Submitted'),
(1107,3,'2025-11-07','11:00','Preparing'),
(1108,2,'2025-11-07','12:30','Ready');

-- 5. "orderItem" 
INSERT INTO "orderItem" ("orders_order_id", "menuItem_menuItem_id", "vendor_id", "price_per_item") VALUES
-- October 1–3
(1001,1001,101,43.90),(1002,1003,101,52.90),(1002,1005,101,32.50),(1003,1002,101,51.90),
(1004,1004,101,52.90),(1005,1001,101,43.90),(1006,1006,101,32.50),(1006,1007,101,59.90),
(1007,1008,101,63.90),(1008,1003,101,52.90),(1008,1005,101,32.50),(1009,1010,101,34.90),
-- October 4–6
(1010,1011,101,34.90),(1011,1012,101,34.90),(1012,1013,101,15.00),(1012,1014,101,20.00),
(1013,1009,101,59.90),(1014,1010,101,34.90),(1015,1015,101,25.00),(1016,1001,101,43.90),
(1017,1002,101,51.90),(1018,1005,101,32.50),
-- October 7–10
(1019,1003,101,52.90),(1020,1004,101,52.90),(1021,1006,101,32.50),(1022,1007,101,59.90),
(1023,1008,101,63.90),(1024,1009,101,59.90),(1025,1010,101,34.90),(1026,1011,101,34.90),
(1027,1012,101,34.90),(1028,1013,101,15.00),(1029,1014,101,20.00),(1030,1015,101,25.00),
-- October 11–14
(1031,1001,101,43.90),(1032,1002,101,51.90),(1033,1003,101,52.90),(1034,1004,101,52.90),
(1035,1005,101,32.50),(1036,1006,101,32.50),(1037,1007,101,59.90),(1038,1008,101,63.90),
(1039,1009,101,59.90),(1040,1010,101,34.90),(1041,1011,101,34.90),(1042,1012,101,34.90),
-- October 15–18
(1043,1013,101,15.00),(1044,1014,101,20.00),(1045,1015,101,25.00),(1046,1001,101,43.90),
(1047,1002,101,51.90),(1048,1003,101,52.90),(1049,1004,101,52.90),(1050,1005,101,32.50),
(1051,1006,101,32.50),(1052,1007,101,59.90),(1053,1008,101,63.90),(1054,1009,101,59.90),
-- October 19–22
(1055,1010,101,34.90),(1056,1011,101,34.90),(1057,1012,101,34.90),(1058,1013,101,15.00),
(1059,1014,101,20.00),(1060,1015,101,25.00),(1061,1001,101,43.90),(1062,1002,101,51.90),
(1063,1003,101,52.90),(1064,1004,101,52.90),(1065,1005,101,32.50),(1066,1006,101,32.50),
-- October 23–26
(1067,1007,101,59.90),(1068,1008,101,63.90),(1069,1009,101,59.90),(1070,1010,101,34.90),
(1071,1011,101,34.90),(1072,1012,101,34.90),(1073,1013,101,15.00),(1074,1014,101,20.00),
(1075,1015,101,25.00),(1076,1001,101,43.90),(1077,1002,101,51.90),(1078,1003,101,52.90),
-- October 27–31
(1079,1004,101,52.90),(1080,1005,101,32.50),(1081,1006,101,32.50),(1082,1007,101,59.90),
(1083,1008,101,63.90),(1084,1009,101,59.90),(1085,1010,101,34.90),(1086,1011,101,34.90),
(1087,1012,101,34.90),(1088,1013,101,15.00),(1089,1014,101,20.00),(1090,1015,101,25.00),
(1091,1001,101,43.90),(1092,1002,101,51.90),(1093,1003,101,52.90),
-- November 1–6
(1094,1004,101,52.90),(1095,1005,101,32.50),(1096,1006,101,32.50),(1097,1007,101,59.90),
(1098,1008,101,63.90),(1099,1009,101,59.90),(1100,1010,101,34.90),(1101,1011,101,34.90),
(1102,1012,101,34.90),(1103,1013,101,15.00),(1104,1014,101,20.00),(1105,1015,101,25.00),
-- November 7 (today)
(1106,1001,101,43.90),(1107,1002,101,51.90),(1108,1003,101,52.90);

