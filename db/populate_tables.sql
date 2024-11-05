-- insert student data
LOAD DATA LOCAL INFILE 'db/students.txt'
INTO TABLE User
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(user_id, first_name, last_name, password, email, role);

-- insert some faculty and TA data for testing purpose
LOAD DATA LOCAL INFILE 'db/faculty.txt'
INTO TABLE User
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(user_id, first_name, last_name, email, password, role);

LOAD DATA LOCAL INFILE 'db/ta.txt'
INTO TABLE User
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(user_id, first_name, last_name, email, password, role);

-- Testing Enrollment

-- inserting Textbooks
LOAD DATA LOCAL INFILE 'db/textbooks.txt'
INTO TABLE ETextBook
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(textbook_id, title);

-- inserting Courses
INSERT IGNORE INTO Course ( course_id,course_title,course_type,faculty_user_id,textbook_id,start_date,end_date,capacity,token)
VALUES ("NCSUOganCSC440F24", "CSC440 Database Systems", "Active", "KeOg1024", 101, "2024-08-15", "2024-12-15", 60, "XYJKLM");
INSERT IGNORE INTO Course ( course_id,course_title,course_type,faculty_user_id,textbook_id,start_date,end_date,capacity,token)
VALUES ("NCSUOganCSC540F24", "CSC540 Database Systems", "Active", "KeOg1024", 101, "2024-08-17", "2024-12-15",50, "STUKZT");
INSERT IGNORE INTO Course ( course_id,course_title,course_type,faculty_user_id,textbook_id,start_date,end_date,capacity,token)
VALUES ("NCSUSaraCSC326F24", "CSC326 Software Engineering", "Active","SaMi1024", 102, "2024-08-23", "2024-10-23", 100,  "LRUFND");
INSERT IGNORE INTO Course ( course_id,course_title,course_type,faculty_user_id,textbook_id,start_date,end_date,capacity,token)
VALUES ("NCSUJegiCSC522F24", "CSC522 Fundamentals of Machine Learning", "Evaluation", "JoDo1024", 103, "2025-08-25", "2025-12-18", NULL, NULL);

-- inserting Enrollments
LOAD DATA LOCAL INFILE 'db/enrollments.txt'
INTO TABLE Enrollment
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(course_id,student_user_id,status);

-- Testing View Section

-- inserting chapter
LOAD DATA LOCAL INFILE 'db/chapters_new.txt'
INTO TABLE Chapter
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(textbook_id,chapter_id,title,is_hidden,created_by);

-- inserting section
LOAD DATA LOCAL INFILE 'db/sections_new.txt'
INTO TABLE Section
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(textbook_id,chapter_id,section_id,title,is_hidden,created_by);

-- inserting contentblock
LOAD DATA LOCAL INFILE 'db/blocks.txt'
INTO TABLE ContentBlock
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(textbook_id,chapter_id,section_id,content_block_id,content_type,content,is_hidden,created_by);


-- inserting into activities
LOAD DATA LOCAL INFILE 'db/activity.txt'
INTO TABLE Activities
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
(textbook_id,chapter_id,section_id,content_block_id,activity_id,is_hidden,created_by);

-- inserting into questions
LOAD DATA LOCAL INFILE 'db/questions.txt'
INTO TABLE Question
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(textbook_id,chapter_id,section_id,content_block_id,activity_id,question_id, question, option1, explanation_op1, option2, explanation_op2, option3, explanation_op3, option4, explanation_op4, correct_answer);
