-- insert student data
LOAD DATA LOCAL INFILE 'db/students.txt'
INTO TABLE User
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(user_id, first_name, last_name, user_password, email, user_role);

LOAD DATA LOCAL INFILE 'db/textbooks.txt'
INTO TABLE ETextBook
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(textbook_id, title);

-- Testing Enrollment

INSERT IGNORE INTO Course ( course_id,course_title,course_type,faculty_user_id,textbook_id,start_date,end_date,capacity,token)
VALUES ("NCSUOganCSC440F24", "CSC440 Database Systems", "Active", "KeOg1024", 101, "2024-08-15", "2024-12-15", 60, "XYJKLM");

INSERT IGNORE INTO Enrollment (course_id, student_user_id, status)
VALUES ('NCSUOganCSC440F24','ErPe1024','Enrolled');