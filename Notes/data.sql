INSERT INTO library_author (name, bio, date_of_birth) VALUES 
('Author 1', 'Bio 1', '1990-01-01'),
('Author 2', 'Bio 2', '1991-01-01'),
('Author 3', 'Bio 3', '1992-01-01'),
('Author 4', 'Bio 4', '1993-01-01');


INSERT INTO library_genre (label) VALUES 
('Science Fiction'),
('Fantasy'),
('Mystery');


INSERT INTO library_book (title, published_date, author_id, rating, is_featured)
VALUES
('Book 1', CURRENT_DATE, 1, 4.5, TRUE),
('Book 2', CURRENT_DATE, 2, 3.8, FALSE),
('Book 3', CURRENT_DATE, 3, 4.2, TRUE),
('Book 4', CURRENT_DATE, 4, 4.9, FALSE),
('Book 5', CURRENT_DATE, 1, 3.5, TRUE),
('Book 6', CURRENT_DATE, 2, 4.0, FALSE),
('Book 7', CURRENT_DATE, 3, 4.7, TRUE),
('Book 8', CURRENT_DATE, 4, 3.9, FALSE),
('Book 9', CURRENT_DATE, 1, 4.1, TRUE),
('Book 10', CURRENT_DATE, 2, 3.6, FALSE),
('Book 11', CURRENT_DATE, 3, 4.3, TRUE),
('Book 12', CURRENT_DATE, 4, 4.8, FALSE),
('Book 13', CURRENT_DATE, 1, 3.7, TRUE),
('Book 14', CURRENT_DATE, 2, 4.4, FALSE),
('Book 15', CURRENT_DATE, 3, 4.5, TRUE),
('Book 16', CURRENT_DATE, 4, 4.2, FALSE),
('Book 17', CURRENT_DATE, 1, 4.9, TRUE),
('Book 18', CURRENT_DATE, 2, 3.8, FALSE),
('Book 19', CURRENT_DATE, 3, 4.0, TRUE),
('Book 20', CURRENT_DATE, 4, 3.5, FALSE),
('Book 21', CURRENT_DATE, 1, 4.6, TRUE),
('Book 22', CURRENT_DATE, 2, 4.1, FALSE),
('Book 23', CURRENT_DATE, 3, 3.9, TRUE),
('Book 24', CURRENT_DATE, 4, 4.3, FALSE),
('Book 25', CURRENT_DATE, 1, 3.4, TRUE),
('Book 26', CURRENT_DATE, 2, 4.7, FALSE),
('Book 27', CURRENT_DATE, 3, 4.8, TRUE),
('Book 28', CURRENT_DATE, 4, 4.0, FALSE),
('Book 29', CURRENT_DATE, 1, 3.6, TRUE),
('Book 30', CURRENT_DATE, 2, 4.5, FALSE);

INSERT INTO library_book_genre (book_id, genre_id)
VALUES
(1, 1), (1, 2),
(2, 2),
(3, 3), (3, 1),
(4, 1),
(5, 2),
(6, 3), (6, 1),
(7, 2),
(8, 1), (8, 3),
(9, 3),
(10, 2),
(11, 1),
(12, 3), (12, 2),
(13, 1),
(14, 2),
(15, 3),
(16, 1),
(17, 2),
(18, 3), (18, 1),
(19, 2),
(20, 1),
(21, 3),
(22, 2),
(23, 1),
(24, 3),
(25, 2),
(26, 1),
(27, 3),
(28, 2),
(29, 1),
(30, 3), (30, 2);


-- UPDATE library_genre SET label = 'Science Fiction' WHERE id = 1;
-- UPDATE library_genre SET label = 'Fantasy' WHERE id = 2;
-- UPDATE library_genre SET label = 'Mystery' WHERE id = 3;