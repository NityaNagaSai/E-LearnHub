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

CREATE TABLE Chapter (
    chapter_id VARCHAR(25),
    textbook_id INT NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    PRIMARY KEY (textbook_id, chapter_id),
    FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL,
    FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id) ON DELETE CASCADE,
    UNIQUE(textbook_id, title)
);

CREATE TABLE Section (
    section_id VARCHAR(25) NOT NULL,
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    section_number INT,
    title VARCHAR(255) NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    PRIMARY KEY (textbook_id, chapter_id, section_id),
    FOREIGN KEY (textbook_id, chapter_id)  REFERENCES Chapter(textbook_id, chapter_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL
);

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

-- CREATE TABLE Question (
--     question_id VARCHAR(25),
--     activity_id VARCHAR(25) NOT NULL,
--     content_block_id VARCHAR(25) NOT NULL,
--     textbook_id INT NOT NULL,
--     section_id VARCHAR(25) NOT NULL,
--     chapter_id VARCHAR(25) NOT NULL,
--     question TEXT NOT NULL,
--     correct_answer VARCHAR(255) NOT NULL,
--     option1 VARCHAR(255) NOT NULL,
--     option2 VARCHAR(255) NOT NULL,
--     option3 VARCHAR(255) NOT NULL,
--     option4 VARCHAR(255) NOT NULL,
--     explanation_op1 VARCHAR(255) NOT NULL,
--     explanation_op2 VARCHAR(255) NOT NULL,
--     explanation_op3 VARCHAR(255) NOT NULL,
--     explanation_op4 VARCHAR(255) NOT NULL,
--     PRIMARY KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id)
--     FOREIGN KEY (textbook_id, chapter_id, section_id, content_block_id) REFERENCES Section(textbook_id, chapter_id, section_id, content_block_id) ON DELETE CASCADE,
--     FOREIGN KEY (activity_id) REFERENCES Activities(activity_id) ON DELETE CASCADE
-- );

-- CREATE TABLE StudentActivityPoint (
--     question_id VARCHAR(25) NOT NULL,
--     answer_activity_id VARCHAR(25) PRIMARY KEY,
--     activity_id VARCHAR(25) NOT NULL,
--     content_block_id VARCHAR(25) NOT NULL,
--     textbook_id INT NOT NULL,
--     section_id VARCHAR(25) NOT NULL,
--     chapter_id VARCHAR(25) NOT NULL,
--     question_points INT,
--     timestamp DATETIME,
--     PRIMARY KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id)
--     FOREIGN KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id) REFERENCES Section(textbook_id, chapter_id, section_id, content_block_id, activity_id) ON DELETE CASCADE,
--     FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE
-- );

-- CREATE TABLE User (
--     user_id VARCHAR(10) PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     password VARCHAR(100) NOT NULL,
--     role ENUM('Admin', 'Faculty', 'Student', 'TA') NOT NULL
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
--     token VARCHAR(255),
--     FOREIGN KEY (faculty_user_id) REFERENCES User(user_id),
--     FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id)
-- );

-- CREATE TABLE Enrollment (
--     course_id VARCHAR(50) NOT NULL,
--     student_user_id VARCHAR(10) NOT NULL,
--     status ENUM('Pending', 'Enrolled') DEFAULT 'Pending',
--     FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
--     FOREIGN KEY (student_user_id) REFERENCES User(user_id) ON DELETE CASCADE,
--     PRIMARY KEY (course_id, student_user_id)
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
--     activity_id VARCHAR(25) NOT NULL,
--     score INT NOT NULL,
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (student_user_id, activity_id),
--     FOREIGN KEY (student_user_id) REFERENCES User(user_id),
--     FOREIGN KEY (activity_id) REFERENCES Activities(activity_id)
-- );