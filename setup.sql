-- script to setup database for deployment

CREATE DATABASE IF NOT EXISTS Astrics;
CREATE USER IF NOT EXISTS 'astrics'@'localhost' IDENTIFIED BY "astrics_pwd";
GRANT ALL PRIVILEGES ON Astrics.* TO 'astrics'@'localhost';
FLUSH PRIVILEGES;
