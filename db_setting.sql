DELETE FROM mysql.user WHERE User = 'vitaldocz';
FLUSH PRIVILEGES;
CREATE USER 'vitaldocz'@'localhost' IDENTIFIED BY 'vitaldocz';
CREATE DATABASE IF NOT EXISTS vitaldocz_blog;
GRANT ALL PRIVILEGES ON *.* TO 'vitaldocz'@'localhost';
FLUSH PRIVILEGES;
