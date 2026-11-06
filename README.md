School Management System

A Python application with a MySQL database for managing students, teachers, courses and course registrations. It has two interfaces: a command-line menu and a desktop GUI built with customtkinter.

Built as my Foundation Year final project at Coventry University Kazakhstan (Software and Databases).

Features
Add, view, search, update and delete students, teachers, courses and registrations
Two ways to use it: a menu in the terminal (main.py) or a graphical interface (gui.py)
Relational MySQL database with four linked tables, foreign keys, unique and check constraints, and indexes
All database operations run through 20 stored procedures (5 per entity: add, update, delete, get all, search)
Input validation and error handling, so bad input shows a clear message instead of crashing
Tech stack
Python 3
MySQL (accessed with mysql-connector-python)
customtkinter for the GUI
Project structure
File	Purpose
main.py	Command-line menus
gui.py	Desktop GUI (customtkinter)
database.py	Database class: MySQL connection and stored-procedure calls
person.py	Person base class (shared name, email and phone fields)
student.py, teacher.py	Student and Teacher classes, which inherit from Person
course.py, registration.py	Course and Registration classes
config.example.py	Template for the database connection settings
SchoolManagementDB final project.sql	Creates the database, tables, stored procedures and sample data
Database design

Four tables:

Teachers: name, unique email, phone, department
Students: name, unique email, phone, date of birth, status (Active, Inactive or Graduated)
Courses: name, description, credits (must be greater than 0), assigned teacher (set to NULL if the teacher is deleted)
Registrations: links a student to a course, with a date and a status (Enrolled, Completed or Dropped); each student can register for a course only once, and a registration is removed if its student or course is deleted
Object-oriented design

Student and Teacher inherit from a shared Person class. Each entity (Student, Teacher, Course, Registration) has its own class with methods for adding, updating, deleting, searching and sorting. A single Database class handles the connection, and all other classes use it.

Setup
Install Python 3 and MySQL, and make sure the MySQL server is running.
Install the Python packages:
bash
   pip install -r requirements.txt
Create the database. Run the SQL file in MySQL Workbench, or from the terminal:
bash
   mysql -u root -p < "SchoolManagementDB final project.sql"
Add your database settings. Copy config.example.py to config.py and enter your own MySQL username and password:
bash
   cp config.example.py config.py
Run the application:
bash
   python main.py     # command-line version
   python gui.py      # graphical version
Screenshots
<!-- Add 2-3 screenshots of the GUI here, for example: ![Students tab](screenshots/students.png) -->
What I learned
Designing a relational database with keys and constraints
Using stored procedures from Python
Structuring a project with classes and inheritance
Building both a text interface and a GUI on the same logic
Author

Aslan Vakpayev: BSc (Hons) Computer Science with Artificial Intelligence, Coventry University Kazakhstan
