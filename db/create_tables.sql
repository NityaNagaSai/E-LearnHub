CREATE TABLE IF NOT EXISTS User (
    user_id VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_password VARCHAR(100) NOT NULL,
    user_role ENUM('Admin', 'Faculty', 'Student', 'TA') NOT NULL
);

CREATE TABLE IF NOT EXISTS ETextBook (
    textbook_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Chapter (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    title VARCHAR(255) NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    PRIMARY KEY (textbook_id, chapter_id),
    FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL,
    FOREIGN KEY (textbook_id) REFERENCES ETextBook(textbook_id) ON DELETE CASCADE,
    UNIQUE(textbook_id, title)
);

CREATE TABLE IF NOT EXISTS Section (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    section_id VARCHAR(25) NOT NULL,
    title VARCHAR(255) NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    PRIMARY KEY (textbook_id, chapter_id, section_id),
    FOREIGN KEY (textbook_id, chapter_id)  REFERENCES Chapter(textbook_id, chapter_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ContentBlock (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    section_id VARCHAR(25) NOT NULL,
    content_block_id VARCHAR(25) NOT NULL,
    content_type ENUM('text', 'image', 'activity') NOT NULL,
    content TEXT NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    PRIMARY KEY (content_block_id, textbook_id, chapter_id, section_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id) REFERENCES Section(textbook_id, chapter_id, section_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Activity (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    section_id VARCHAR(25) NOT NULL,
    content_block_id VARCHAR(25) NOT NULL,
    activity_id VARCHAR(25) NOT NULL,
    is_hidden ENUM('yes', 'no') NOT NULL,
    created_by VARCHAR(255),
    PRIMARY KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id, content_block_id) REFERENCES ContentBlock(textbook_id, chapter_id, section_id, content_block_id) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS Question (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    section_id VARCHAR(25) NOT NULL,
    content_block_id VARCHAR(25) NOT NULL,
    activity_id VARCHAR(25) NOT NULL,
    question_id VARCHAR(25) NOT NULL,
    question TEXT NOT NULL,
    option1 VARCHAR(255) NOT NULL,
    explanation_op1 VARCHAR(255) NOT NULL,
    option2 VARCHAR(255) NOT NULL,
    explanation_op2 VARCHAR(255) NOT NULL,
    option3 VARCHAR(255) NOT NULL,
    explanation_op3 VARCHAR(255) NOT NULL,
    option4 VARCHAR(255) NOT NULL,
    explanation_op4 VARCHAR(255) NOT NULL,
    correct_answer VARCHAR(255) NOT NULL,
    PRIMARY KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id) 
    REFERENCES Activity(textbook_id, chapter_id, section_id, content_block_id, activity_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Course (
    course_id VARCHAR(50) PRIMARY KEY,
    course_title VARCHAR(255) NOT NULL,
    course_type ENUM('Active', 'Evaluation') NOT NULL,
    faculty_user_id VARCHAR(255) NOT NULL,
    ta_user_id VARCHAR(255),
    textbook_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    capacity INT,
    token VARCHAR(255),
    FOREIGN KEY (faculty_user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (ta_user_id) REFERENCES User(user_id) ON DELETE SET NULL,
    FOREIGN KEY (textbook_id) REFERENCES ETextBook (textbook_id)
);

CREATE TABLE IF NOT EXISTS StudentActivityPoint (
    student_id VARCHAR(255) NOT NULL,
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(25) NOT NULL,
    section_id VARCHAR(25) NOT NULL,
    content_block_id VARCHAR(25) NOT NULL,
    activity_id VARCHAR(25) NOT NULL,
    question_id VARCHAR(25) NOT NULL,
    question_points INT,
    timestamp DATETIME NOT NULL,
    PRIMARY KEY (student_id, textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id) 
        REFERENCES Question(textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Enrollment (
    course_id VARCHAR(50) NOT NULL,
    student_user_id VARCHAR(255) NOT NULL,
    status ENUM('Pending', 'Enrolled') DEFAULT 'Pending',
    PRIMARY KEY (course_id, student_user_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (student_user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS StudentParticipation (
    student_id VARCHAR(255) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    participation_points INT NOT NULL,
    finished_activities INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TeachingAssistantAssignment (
    course_id VARCHAR(50) NOT NULL,
    ta_user_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (course_id, ta_user_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (ta_user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Notification (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);


DELIMITER //

-- Trigger 1: Automatically Create an Enrollment Record When a Student is Assigned to a Course

CREATE TRIGGER after_student_enrollment
AFTER INSERT ON Enrollment
FOR EACH ROW
BEGIN
    IF NEW.status = 'Enrolled' THEN
        INSERT INTO StudentParticipation (student_id, course_id, participation_points, finished_activities)
        VALUES (NEW.student_user_id, NEW.course_id, 0, 0);
    END IF;
END//

-- Trigger 2: Update `is_read` Status on Notification
CREATE TRIGGER after_notification_access
AFTER SELECT ON Notification
FOR EACH ROW
BEGIN
    IF OLD.is_read = FALSE THEN
        UPDATE Notification
        SET is_read = TRUE
        WHERE notification_id = OLD.notification_id;
    END IF;
END//

-- Procedure: Enroll Student in a Course
CREATE PROCEDURE EnrollStudent(
    IN p_student_id VARCHAR(255),
    IN p_course_id VARCHAR(50),
    OUT p_status_message VARCHAR(255)
)
BEGIN
    DECLARE course_capacity INT DEFAULT 0;
    DECLARE enrolled_count INT DEFAULT 0;

    -- Check if the course exists and retrieve capacity
    SELECT capacity INTO course_capacity
    FROM Course
    WHERE course_id = p_course_id;

    IF course_capacity IS NULL THEN
        SET p_status_message = 'Course does not exist';
    ELSE
        -- Check current enrollment count
        SELECT COUNT(*) INTO enrolled_count
        FROM Enrollment
        WHERE course_id = p_course_id AND status = 'Enrolled';

        IF enrolled_count >= course_capacity THEN
            SET p_status_message = 'Course is full';
        ELSE
            -- Insert enrollment record
            INSERT INTO Enrollment (course_id, student_user_id, status)
            VALUES (p_course_id, p_student_id, 'Enrolled')
            ON DUPLICATE KEY UPDATE status = 'Enrolled';

            -- Insert initial participation record
            INSERT INTO StudentParticipation (student_id, course_id, participation_points, finished_activities)
            VALUES (p_student_id, p_course_id, 0, 0)
            ON DUPLICATE KEY UPDATE participation_points = 0, finished_activities = 0;

            SET p_status_message = 'Enrollment successful';
        END IF;
    END IF;
END//

DELIMITER ;
