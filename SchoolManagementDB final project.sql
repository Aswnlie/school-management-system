-- =============================================================
-- 1. CREATE DATABASE
-- =============================================================

CREATE DATABASE IF NOT EXISTS SchoolManagementDB
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE SchoolManagementDB;


-- =============================================================
-- 2. TABLES
-- =============================================================

CREATE TABLE IF NOT EXISTS Teachers (
    TeacherID INT AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName  VARCHAR(50) NOT NULL,
    Email     VARCHAR(100) NOT NULL,
    Phone     VARCHAR(20),
    Department VARCHAR(100) NOT NULL,
    PRIMARY KEY (TeacherID),
    UNIQUE KEY uq_teacher_email (Email)
);

CREATE TABLE IF NOT EXISTS Students (
    StudentID INT AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName  VARCHAR(50) NOT NULL,
    Email     VARCHAR(100) NOT NULL,
    Phone     VARCHAR(20),
    DateOfBirth DATE,
    Status VARCHAR(20) NOT NULL DEFAULT 'Active',
    PRIMARY KEY (StudentID),
    UNIQUE KEY uq_student_email (Email),
    CONSTRAINT chk_student_status
        CHECK (Status IN ('Active','Inactive','Graduated'))
);

CREATE TABLE IF NOT EXISTS Courses (
    CourseID INT AUTO_INCREMENT,
    CourseName VARCHAR(100) NOT NULL,
    Description TEXT,
    Credits INT NOT NULL DEFAULT 1,
    TeacherID INT,
    PRIMARY KEY (CourseID),
    CONSTRAINT chk_credits CHECK (Credits > 0),
    CONSTRAINT fk_course_teacher
        FOREIGN KEY (TeacherID)
        REFERENCES Teachers(TeacherID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Registrations (
    RegistrationID INT AUTO_INCREMENT,
    StudentID INT NOT NULL,
    CourseID  INT NOT NULL,
    RegistrationDate DATE NOT NULL DEFAULT CURRENT_DATE,
    Status VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    PRIMARY KEY (RegistrationID),
    UNIQUE KEY uq_student_course (StudentID, CourseID),
    CONSTRAINT chk_reg_status
        CHECK (Status IN ('Enrolled','Completed','Dropped')),
    CONSTRAINT fk_reg_student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_reg_course
        FOREIGN KEY (CourseID)
        REFERENCES Courses(CourseID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Indexes (correct syntax)
CREATE INDEX idx_reg_student ON Registrations(StudentID);
CREATE INDEX idx_reg_course  ON Registrations(CourseID);


-- =============================================================
-- 3. STORED PROCEDURES
-- =============================================================


-- ================= STUDENTS =================

CREATE PROCEDURE AddStudent(
    IN p_FirstName VARCHAR(50),
    IN p_LastName  VARCHAR(50),
    IN p_Email     VARCHAR(100),
    IN p_Phone     VARCHAR(20),
    IN p_DateOfBirth DATE
)
BEGIN
    INSERT INTO Students (FirstName, LastName, Email, Phone, DateOfBirth)
    VALUES (p_FirstName, p_LastName, p_Email, p_Phone, p_DateOfBirth);
END


CREATE PROCEDURE UpdateStudent(
    IN p_StudentID INT,
    IN p_FirstName VARCHAR(50),
    IN p_LastName  VARCHAR(50),
    IN p_Email     VARCHAR(100),
    IN p_Phone     VARCHAR(20),
    IN p_DateOfBirth DATE,
    IN p_Status VARCHAR(20)
)
BEGIN
    UPDATE Students
    SET FirstName = p_FirstName,
        LastName  = p_LastName,
        Email     = p_Email,
        Phone     = p_Phone,
        DateOfBirth = p_DateOfBirth,
        Status = p_Status
    WHERE StudentID = p_StudentID;
END$$


CREATE PROCEDURE DeleteStudent(IN p_StudentID INT)
BEGIN
    DELETE FROM Students WHERE StudentID = p_StudentID;
END$$


CREATE PROCEDURE GetAllStudents()
BEGIN
    SELECT * FROM Students;
END$$


CREATE PROCEDURE SearchStudent(IN p_SearchTerm VARCHAR(100))
BEGIN
    SELECT * FROM Students
    WHERE FirstName LIKE CONCAT('%', p_SearchTerm, '%')
       OR LastName  LIKE CONCAT('%', p_SearchTerm, '%');
END$$


-- ================= TEACHERS =================

CREATE PROCEDURE AddTeacher(
    IN p_FirstName VARCHAR(50),
    IN p_LastName  VARCHAR(50),
    IN p_Email     VARCHAR(100),
    IN p_Phone     VARCHAR(20),
    IN p_Department VARCHAR(100)
)
BEGIN
    INSERT INTO Teachers (FirstName, LastName, Email, Phone, Department)
    VALUES (p_FirstName, p_LastName, p_Email, p_Phone, p_Department);
END$$


CREATE PROCEDURE UpdateTeacher(
    IN p_TeacherID INT,
    IN p_FirstName VARCHAR(50),
    IN p_LastName  VARCHAR(50),
    IN p_Email     VARCHAR(100),
    IN p_Phone     VARCHAR(20),
    IN p_Department VARCHAR(100)
)
BEGIN
    UPDATE Teachers
    SET FirstName=p_FirstName,
        LastName=p_LastName,
        Email=p_Email,
        Phone=p_Phone,
        Department=p_Department
    WHERE TeacherID=p_TeacherID;
END$$


CREATE PROCEDURE DeleteTeacher(IN p_TeacherID INT)
BEGIN
    DELETE FROM Teachers WHERE TeacherID=p_TeacherID;
END$$


CREATE PROCEDURE GetAllTeachers()
BEGIN
    SELECT * FROM Teachers;
END$$


CREATE PROCEDURE SearchTeacher(IN p_SearchTerm VARCHAR(100))
BEGIN
    SELECT * FROM Teachers
    WHERE FirstName LIKE CONCAT('%', p_SearchTerm, '%')
       OR LastName  LIKE CONCAT('%', p_SearchTerm, '%');
END$$


-- ================= COURSES =================

CREATE PROCEDURE AddCourse(
    IN p_CourseName VARCHAR(100),
    IN p_Description TEXT,
    IN p_Credits INT,
    IN p_TeacherID INT
)
BEGIN
    INSERT INTO Courses (CourseName, Description, Credits, TeacherID)
    VALUES (p_CourseName, p_Description, p_Credits, p_TeacherID);
END$$


CREATE PROCEDURE UpdateCourse(
    IN p_CourseID INT,
    IN p_CourseName VARCHAR(100),
    IN p_Description TEXT,
    IN p_Credits INT,
    IN p_TeacherID INT
)
BEGIN
    UPDATE Courses
    SET CourseName=p_CourseName,
        Description=p_Description,
        Credits=p_Credits,
        TeacherID=p_TeacherID
    WHERE CourseID=p_CourseID;
END$$


CREATE PROCEDURE DeleteCourse(IN p_CourseID INT)
BEGIN
    DELETE FROM Courses WHERE CourseID=p_CourseID;
END$$


CREATE PROCEDURE GetAllCourses()
BEGIN
    SELECT * FROM Courses;
END$$


CREATE PROCEDURE SearchCourse(IN p_SearchTerm VARCHAR(100))
BEGIN
    SELECT * FROM Courses
    WHERE CourseName LIKE CONCAT('%', p_SearchTerm, '%');
END$$


-- ================= REGISTRATIONS =================

CREATE PROCEDURE AddRegistration(
    IN p_StudentID INT,
    IN p_CourseID INT
)
BEGIN
    INSERT INTO Registrations (StudentID, CourseID)
    VALUES (p_StudentID, p_CourseID);
END$$


CREATE PROCEDURE UpdateRegistration(
    IN p_RegistrationID INT,
    IN p_StudentID INT,
    IN p_CourseID INT,
    IN p_RegistrationDate DATE,
    IN p_Status VARCHAR(20)
)
BEGIN
    UPDATE Registrations
    SET StudentID = p_StudentID,
        CourseID = p_CourseID,
        RegistrationDate = p_RegistrationDate,
        Status = p_Status
    WHERE RegistrationID = p_RegistrationID;
END$$


CREATE PROCEDURE DeleteRegistration(IN p_RegistrationID INT)
BEGIN
    DELETE FROM Registrations WHERE RegistrationID=p_RegistrationID;
END$$


CREATE PROCEDURE GetAllRegistrations()
BEGIN
    SELECT
        r.RegistrationID,
        CONCAT(s.FirstName,' ',s.LastName),
        c.CourseName,
        r.RegistrationDate,
        r.Status
    FROM Registrations r
    JOIN Students s ON r.StudentID=s.StudentID
    JOIN Courses c  ON r.CourseID=c.CourseID;
END$$


CREATE PROCEDURE SearchRegistration(IN p_SearchTerm VARCHAR(100))
BEGIN
    SELECT * FROM Registrations
    WHERE RegistrationID = p_SearchTerm;
END$$

DELIMITER ;


-- =============================================================
-- 4. SAMPLE DATA
-- =============================================================

INSERT INTO Teachers (FirstName,LastName,Email,Phone,Department) VALUES
('Sarah','Johnson','sarah@school.com','555-0101','CS');

INSERT INTO Students (FirstName,LastName,Email,Phone,DateOfBirth) VALUES
('Alice','Smith','alice@email.com','555-1001','2003-04-15');

INSERT INTO Courses (CourseName,Credits,TeacherID) VALUES
('Python',3,1);

INSERT INTO Registrations (StudentID,CourseID) VALUES (1,1);
```