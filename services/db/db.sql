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
	book_id INT NOT NULL,
	goodreads_book_id INT,
	isbn CHAR(13) DEFAULT NULL,
	author VARCHAR(250) DEFAULT NULL,
	original_publication_year YEAR DEFAULT 0,
	title VARCHAR(500),
	ratings DOUBLE DEFAULT 0.0,
	ratings_count INT DEFAULT 0,
	image_url TEXT DEFAULT NULL,
	source ENUM('GOODREADS'),
	PRIMARY KEY (book_id)
);

CREATE TABLE tags (
	tag_id INT NOT NULL,
	tag VARCHAR(250),
	uber_label VARCHAR(250) DEFAULT NULL,
	PRIMARY KEY (tag_id)
);

INSERT INTO books (author, title, ratings, rating_count) VALUES('Andrew S Tanenbaum','Distributed Systems', 1.5, 19);
INSERT INTO books (author, title, ratings, rating_count) VALUES('Galvin','Operating Systems', 4.5, 900);

CREATE TABLE user_book_mapping (
	user_id INT,
	book_id INT,
	user_feedback BOOLEAN,
	confidence_score DOUBLE,
	is_deleted BOOLEAN,
	PRIMARY KEY (user_id,book_id)
);

CREATE TABLE books_tags_mapping (
	book_id INT NOT NULL,
	tag_id INT NOT NULL,
	id INT NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (id)
);

CREATE TABLE user_interests (
	user_id INT NOT NULL,
	label VARCHAR(250),
	affinity_score DOUBLE,
	PRIMARY KEY (user_id,label)
);

INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(1,1,true);
INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(2,1,false);
INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(1,2,true);
INSERT INTO user_book_mapping (user_id, book_id, user_feedback) VALUES(2,2,false);

