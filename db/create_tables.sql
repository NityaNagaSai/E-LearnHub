CREATE TABLE User (
    user_id VARCHAR(10) PRIMARY KEY,  
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_password VARCHAR(100) NOT NULL,
    user_role ENUM('Admin', 'Faculty', 'Student', 'TA') NOT NULL
);

CREATE TABLE ETextbook (
    textbook_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);


-- CREATE TABLE Chapter (
--     chapter_id INT PRIMARY KEY,
--     textbook_id INT NOT NULL,
--     chapter_number VARCHAR(6) NOT NULL,  
--     title VARCHAR(255) NOT NULL,
--     FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id) ON DELETE CASCADE,
--     UNIQUE(textbook_id, chapter_number),  
--     UNIQUE(textbook_id, title) 
-- );


-- CREATE TABLE Section (
--     section_id INT PRIMARY KEY,
--     chapter_id INT NOT NULL,
--     section_number INT NOT NULL,  
--     title VARCHAR(255) NOT NULL,
--     FOREIGN KEY (chapter_id) REFERENCES Chapter(chapter_id) ON DELETE CASCADE,
--     UNIQUE(chapter_id, section_number)  
-- );


-- CREATE TABLE ContentBlock (
--     content_block_id INT PRIMARY KEY AUTO_INCREMENT,
--     section_id INT NOT NULL,
--     content_type ENUM('text', 'image') NOT NULL,
--     content TEXT NOT NULL,  
--     sequence_number INT NOT NULL,
--     FOREIGN KEY (section_id) REFERENCES Section(section_id) ON DELETE CASCADE,
--     UNIQUE(section_id, content_block_id)  
-- );

-- CREATE TABLE Activities (
--     activity_id INT PRIMARY KEY AUTO_INCREMENT,
--     content_block_id INT NOT NULL UNIQUE,  
--     question TEXT NOT NULL,
--     correct_answer VARCHAR(255) NOT NULL,
--     incorrect_answer1 VARCHAR(255) NOT NULL,
--     incorrect_answer2 VARCHAR(255) NOT NULL,
--     incorrect_answer3 VARCHAR(255) NOT NULL,
--     explanation_correct VARCHAR(255) NOT NULL,
--     explanation_incorrect1 VARCHAR(255) NOT NULL,
--     explanation_incorrect2 VARCHAR(255) NOT NULL,
--     explanation_incorrect3 VARCHAR(255) NOT NULL,
--     FOREIGN KEY (content_block_id) REFERENCES ContentBlock(content_block_id),
--     UNIQUE(content_block_id, activity_id)  
-- );



-- CREATE TABLE Course (
--     course_id VARCHAR(50) PRIMARY KEY,
--     course_title VARCHAR(255) NOT NULL,
--     course_type ENUM('Active', 'Evaluation') NOT NULL,
--     faculty_user_id VARCHAR(10) NOT NULL,  
--     textbook_id INT NOT NULL,  
--     start_date DATE,
--     end_date DATE,
--     capacity INT,
--     FOREIGN KEY (faculty_user_id) REFERENCES User(user_id),
--     FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id)
-- );

-- CREATE TABLE Enrollment (
--     enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
--     course_id VARCHAR(50) NOT NULL,
--     student_user_id VARCHAR(10) NOT NULL,
--     status ENUM('Pending', ‘Enrolled’) DEFAULT 'Pending',  
--     FOREIGN KEY (course_id) REFERENCES Course(course_id),
--     FOREIGN KEY (student_user_id) REFERENCES User(user_id),
--     UNIQUE(course_id, student_user_id)  
-- );

-- CREATE TABLE TeachingAssistantAssignment (
--     course_id VARCHAR(50) NOT NULL,
--     ta_user_id VARCHAR(10) NOT NULL, 
--     PRIMARY KEY (course_id, ta_user_id),
--     FOREIGN KEY (course_id) REFERENCES Course(course_id),
--     FOREIGN KEY (ta_user_id) REFERENCES User(user_id)
-- );

-- CREATE TABLE Notification (
--     notification_id INT PRIMARY KEY AUTO_INCREMENT,
--     user_id VARCHAR(10) NOT NULL,
--     message TEXT NOT NULL,
--     is_read BOOLEAN DEFAULT FALSE,
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES User(user_id)
-- );

-- CREATE TABLE StudentActivity (
--     student_user_id VARCHAR(10) NOT NULL,
--     activity_id INT NOT NULL,
--     score INT NOT NULL,  
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (student_user_id, activity_id)
--     FOREIGN KEY (student_user_id) REFERENCES User(user_id),
--     FOREIGN KEY (activity_id) REFERENCES Activities(activity_id)
-- );
