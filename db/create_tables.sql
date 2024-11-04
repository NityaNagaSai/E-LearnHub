-- CREATE TABLE User (
--     user_id VARCHAR(10) PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     password VARCHAR(100) NOT NULL,
--     role ENUM('Admin', 'Faculty', 'Student', 'TA') NOT NULL
-- );

-- CREATE TABLE ETextbook (
--     textbook_id INT PRIMARY KEY,
--     title VARCHAR(255) NOT NULL
-- );

-- CREATE TABLE Chapter (
--     chapter_id VARCHAR(25),
--     textbook_id INT NOT NULL,
--     is_hidden ENUM('yes', 'no') NOT NULL,
--     created_by VARCHAR(255),
--     title VARCHAR(255) NOT NULL,
--     PRIMARY KEY (textbook_id, chapter_id),
--     FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL,
--     FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id) ON DELETE CASCADE,
--     UNIQUE(textbook_id, title)
-- );

-- CREATE TABLE Section (
--     section_id VARCHAR(25) NOT NULL,
--     textbook_id INT NOT NULL,
--     chapter_id VARCHAR(25) NOT NULL,
--     section_number INT,
--     title VARCHAR(255) NOT NULL,
--     is_hidden ENUM('yes', 'no') NOT NULL,
--     created_by VARCHAR(255),
--     PRIMARY KEY (textbook_id, chapter_id, section_id),
--     FOREIGN KEY (textbook_id, chapter_id)  REFERENCES Chapter(textbook_id, chapter_id) ON DELETE CASCADE,
--     FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL
-- );

CREATE TABLE ContentBlock (
    content_block_id VARCHAR(25),
    textbook_id INT NOT NULL,
    section_id VARCHAR(25) NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    content_type ENUM('text', 'image') NOT NULL,
    content TEXT NOT NULL,
    sequence_number INT NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    PRIMARY KEY (textbook_id, chapter_id, section_id, content_block_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id) REFERENCES Section(textbook_id, chapter_id, section_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL
);