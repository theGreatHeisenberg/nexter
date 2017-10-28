create database nexter;

CREATE TABLE users (
	user_id INT NOT NULL AUTO_INCREMENT,
	twitter_handle VARCHAR(16) NOT NULL,
	created_on DATETIME,
	last_synced DATETIME,
	is_deleted BOOLEAN,
	PRIMARY KEY (user_id)
);

INSERT INTO users (twitter_handle, is_deleted) VALUES('@pankajtekwani12', false);
INSERT INTO users (twitter_handle, is_deleted) VALUES('@kapiltekwani', false);
INSERT INTO users (twitter_handle, is_deleted) VALUES('@shreyas', false);

CREATE TABLE books (
	book_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	goodreads_book_id INT,
	isbn CHAR(13),
	author VARCHAR(256),
	title VARCHAR(500),
	ratings DOUBLE,
	source ENUM('GOODREADS'),
	rating_count INT,
	image_url TEXT,
	original_publication_year YEAR(4)
);

INSERT INTO books (author, title, ratings, rating_count) VALUES('Andrew S Tanenbaum','Distributed Systems', 1.5, 19);
INSERT INTO books (author, title, ratings, rating_count) VALUES('Galvin','Operating Systems', 4.5, 900);

CREATE TABLE user_book_mapping (
	mapping_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
	book_id INT,
	user_feedback BOOLEAN,
	confidence_score DOUBLE,
	is_deleted BOOLEAN
);

INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(1,1,true);
INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(2,1,false);
INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(1,2,true);
INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(2,2,false);
