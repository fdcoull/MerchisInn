-- Drop existing tables
DROP TABLE if EXISTS customers;
DROP TABLE if EXISTS bookings;
DROP TABLE if EXISTS rooms;
DROP TABLE if EXISTS allocations;
DROP TABLE if EXISTS admins;

-- Create tables
CREATE TABLE customers ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        first_name TEXT,
        last_name TEXT
);

CREATE TABLE bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
	room_id INTEGER,
        check_in TEXT,
        check_out TEXT,
        no_guests INTEGER,
        accessible INTEGER,
	price REAL
);

CREATE TABLE rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        no_king INTEGER,
        no_single INTEGER,
        accessible INTEGER
);

CREATE TABLE admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
);

-- King rooms
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 0, 0);
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 0, 0);
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 0, 0);
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 0, 0);
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 0, 0);

-- King and single rooms
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 1, 0);
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 1, 0);

-- Family rooms
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 2, 0);
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 2, 0);

-- Accessible rooms
INSERT INTO rooms (no_king, no_single, accessible) VALUES (2, 2, 1);
