CREATE USER
IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON array_storage.* TO 'user'@'localhost';

CREATE DATABASE
IF NOT EXISTS array_storage;

CREATE TABLE
IF NOT EXISTS array_storage.unsorted_arrays
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    array_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE
IF NOT EXISTS array_storage.sorted_arrays
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    array_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
