# =============================================================
# main.py
# Entry point for the School Management System.
# Handles all menus and user interaction.
# All database operations are wrapped in try/except so errors
# are shown cleanly instead of crashing the program.
# =============================================================
 
from database import Database
from student import Student
from teacher import Teacher
from course import Course
from registration import Registration
 
 
def print_header():
    print("\n" + "=" * 50)
    print("     SCHOOL MANAGEMENT SYSTEM")
    print("=" * 50)
 
 
def get_valid_input(prompt, allow_empty=False):
    """Prompt the user until a non-empty string is entered."""
    while True:
        value = input(f"{prompt} ").strip()
        if value or allow_empty:
            return value
        print("This field cannot be empty. Please try again.")
 
 
def get_valid_int(prompt):
    """Prompt the user until a valid integer is entered."""
    while True:
        try:
            return int(input(f"{prompt} ").strip())
        except ValueError:
            print("Please enter a valid whole number.")
 
 
def display_table(rows, headers):
    """Format and print database rows as a readable aligned table."""
    if not rows:
        print("No records found.")
        return
    # If a single tuple was returned instead of a list, wrap it
    if isinstance(rows, tuple):
        rows = [rows]
    col_width = 22
    total_width = col_width * len(headers)
    print("\n" + "-" * total_width)
    print(" | ".join(f"{h:<{col_width}}" for h in headers))
    print("-" * total_width)
    for row in rows:
        print(" | ".join(f"{str(col):<{col_width}}" for col in row))
    print("-" * total_width + "\n")
 
 
# =============================================================
# STUDENT MENU
# =============================================================
 
def student_menu(db):
    while True:
        print("\n--- Student Management ---")
        print("1. View all students")
        print("2. Search student")
        print("3. Add new student")
        print("4. Update student")
        print("5. Delete student")
        print("0. Back")
        choice = input("Your choice: ").strip()
 
        if choice == "1":
            try:
                rows = Student.get_all(db)
                sorted_rows = Student.sort_by_name(rows)
                display_table(sorted_rows, ["ID", "First Name", "Last Name", "Email", "Phone", "DOB", "Status"])
            except Exception as e:
                print(f"Error retrieving students: {e}")
 
        elif choice == "2":
            try:
                term = get_valid_input("Enter name or ID:")
                rows = Student.search(term, db)
                display_table(rows, ["ID", "First Name", "Last Name", "Email", "Phone", "DOB", "Status"])
            except Exception as e:
                print(f"Error searching students: {e}")
 
        elif choice == "3":
            try:
                first = get_valid_input("First name:")
                last  = get_valid_input("Last name:")
                email = get_valid_input("Email:")
                phone = input("Phone (optional): ").strip() or None
                dob   = input("Date of birth (YYYY-MM-DD, optional): ").strip() or None
                student = Student(first, last, email, phone, dob)
                student.add(db)
                print("Student added successfully.")
            except Exception as e:
                print(f"Could not add student: {e}")
 
        elif choice == "4":
            try:
                sid   = get_valid_int("Student ID to update:")
                first = get_valid_input("New first name:")
                last  = get_valid_input("New last name:")
                email = get_valid_input("New email:")
                phone = input("New phone (optional): ").strip() or None
                dob   = input("New date of birth (YYYY-MM-DD, leave blank to keep): ").strip() or None
                print("Status options: Active | Inactive | Graduated")
                status = get_valid_input("New status:")
                student = Student(first, last, email, phone,
                                  date_of_birth=dob, student_id=sid, status=status)
                student.update(db)
                print("Student updated successfully.")
            except Exception as e:
                print(f"Could not update student: {e}")
 
        elif choice == "5":
            try:
                sid = get_valid_int("Student ID to delete:")
                Student.delete_by_id(sid, db)
                print("Student deleted successfully.")
            except Exception as e:
                print(f"Could not delete student: {e}")
 
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
 
 
# =============================================================
# TEACHER MENU
# =============================================================
 
def teacher_menu(db):
    while True:
        print("\n--- Teacher Management ---")
        print("1. View all teachers")
        print("2. Search teacher")
        print("3. Add new teacher")
        print("4. Update teacher")
        print("5. Delete teacher")
        print("0. Back")
        choice = input("Your choice: ").strip()
 
        if choice == "1":
            try:
                rows = Teacher.get_all(db)
                sorted_rows = Teacher.sort_by_name(rows)
                display_table(sorted_rows, ["ID", "First Name", "Last Name", "Email", "Phone", "Department"])
            except Exception as e:
                print(f"Error retrieving teachers: {e}")
 
        elif choice == "2":
            try:
                term = get_valid_input("Enter name or department:")
                rows = Teacher.search(term, db)
                display_table(rows, ["ID", "First Name", "Last Name", "Email", "Phone", "Department"])
            except Exception as e:
                print(f"Error searching teachers: {e}")
 
        elif choice == "3":
            try:
                first = get_valid_input("First name:")
                last  = get_valid_input("Last name:")
                email = get_valid_input("Email:")
                phone = input("Phone (optional): ").strip() or None
                dept  = get_valid_input("Department:")
                teacher = Teacher(first, last, email, phone, dept)
                teacher.add(db)
                print("Teacher added successfully.")
            except Exception as e:
                print(f"Could not add teacher: {e}")
 
        elif choice == "4":
            try:
                tid   = get_valid_int("Teacher ID to update:")
                first = get_valid_input("New first name:")
                last  = get_valid_input("New last name:")
                email = get_valid_input("New email:")
                phone = input("New phone (optional): ").strip() or None
                dept  = get_valid_input("New department:")
                teacher = Teacher(first, last, email, phone, dept, teacher_id=tid)
                teacher.update(db)
                print("Teacher updated successfully.")
            except Exception as e:
                print(f"Could not update teacher: {e}")
 
        elif choice == "5":
            try:
                tid = get_valid_int("Teacher ID to delete:")
                Teacher.delete_by_id(tid, db)
                print("Teacher deleted successfully.")
            except Exception as e:
                print(f"Could not delete teacher: {e}")
 
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
 
 
# =============================================================
# COURSE MENU
# =============================================================
 
def course_menu(db):
    while True:
        print("\n--- Course Management ---")
        print("1. View all courses")
        print("2. Search course")
        print("3. Add new course")
        print("4. Update course")
        print("5. Delete course")
        print("0. Back")
        choice = input("Your choice: ").strip()
 
        if choice == "1":
            try:
                rows = Course.get_all(db)
                sorted_rows = Course.sort_by_name(rows)
                display_table(sorted_rows, ["ID", "Course Name", "Description", "Credits", "Teacher"])
            except Exception as e:
                print(f"Error retrieving courses: {e}")
 
        elif choice == "2":
            try:
                term = get_valid_input("Enter course name or ID:")
                rows = Course.search(term, db)
                display_table(rows, ["ID", "Course Name", "Description", "Credits", "Teacher"])
            except Exception as e:
                print(f"Error searching courses: {e}")
 
        elif choice == "3":
            try:
                name    = get_valid_input("Course name:")
                desc    = input("Description (optional): ").strip() or None
                credits = get_valid_int("Credits:")
                # Show available teachers so the user knows what IDs exist
                print("\nAvailable teachers:")
                display_table(Teacher.get_all(db), ["ID", "First Name", "Last Name", "Email", "Phone", "Department"])
                tid  = get_valid_int("Teacher ID:")
                course = Course(name, desc, credits, tid)
                course.add(db)
                print("Course added successfully.")
            except Exception as e:
                print(f"Could not add course: {e}")
 
        elif choice == "4":
            try:
                # Show existing courses and teachers so the user can pick IDs
                print("\nExisting courses:")
                display_table(Course.get_all(db), ["ID", "Course Name", "Description", "Credits", "Teacher"])
                cid  = get_valid_int("Course ID to update:")
                name = get_valid_input("New course name:")
                desc = input("New description (optional): ").strip() or None
                credits = get_valid_int("New credits:")
                print("\nAvailable teachers:")
                display_table(Teacher.get_all(db), ["ID", "First Name", "Last Name", "Email", "Phone", "Department"])
                tid  = get_valid_int("New teacher ID:")
                course = Course(name, desc, credits, tid, course_id=cid)
                course.update(db)
                print("Course updated successfully.")
            except Exception as e:
                print(f"Could not update course: {e}")
 
        elif choice == "5":
            try:
                cid = get_valid_int("Course ID to delete:")
                Course.delete_by_id(cid, db)
                print("Course deleted successfully.")
            except Exception as e:
                print(f"Could not delete course: {e}")
 
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
 
 
# =============================================================
# REGISTRATION MENU
# =============================================================
 
def registration_menu(db):
    while True:
        print("\n--- Registration Management ---")
        print("1. View all registrations")
        print("2. Search registration")
        print("3. Add new registration")
        print("4. Update registration ")
        print("5. Delete registration")
        print("0. Back")
        choice = input("Your choice: ").strip()
 
        if choice == "1":
            try:
                rows = Registration.get_all(db)
                sorted_rows = Registration.sort_by_date(rows)
                display_table(sorted_rows, ["ID", "Student Name", "Course", "Date", "Status"])
            except Exception as e:
                print(f"Error retrieving registrations: {e}")
 
        elif choice == "2":
            try:
                term = get_valid_input("Enter student name, course name, or registration ID:")
                rows = Registration.search(term, db)
                display_table(rows, ["ID", "Student Name", "Course", "Date", "Status"])
            except Exception as e:
                print(f"Error searching registrations: {e}")
 
        elif choice == "3":
            try:
                # Show students and courses so the user can pick valid IDs
                print("\nAvailable students:")
                display_table(Student.get_all(db), ["ID", "First Name", "Last Name", "Email", "Phone", "DOB", "Status"])
                sid = get_valid_int("Student ID:")
                print("\nAvailable courses:")
                display_table(Course.get_all(db), ["ID", "Course Name", "Description", "Credits", "Teacher"])
                cid = get_valid_int("Course ID:")
                reg = Registration(sid, cid)
                reg.add(db)
                print("Registration added successfully.")
            except Exception as e:
                print(f"Could not add registration: {e}")
 
        elif choice == "4":
            try:
                rid = get_valid_int("Registration ID to update:")

                print("\nAvailable students:")
                display_table(
                    Student.get_all(db),
                    ["ID", "First Name", "Last Name", "Email", "Phone", "DOB", "Status"]
                )
                sid = get_valid_int("New student ID:")

                print("\nAvailable courses:")
                display_table(
                    Course.get_all(db),
                    ["ID", "Course Name", "Description", "Credits", "Teacher"]
                )
                cid = get_valid_int("New course ID:")

                date = get_valid_input("New registration date (YYYY-MM-DD):")
                status = get_valid_input("New status (Enrolled / Completed / Dropped):")

                reg = Registration(
                    sid,
                    cid,
                    registration_id=rid,
                    registration_date=date,
                    status=status
                )

                reg.update(db)
                print("Registration updated successfully.")

            except Exception as e:
                print(f"Could not update registration: {e}") 
 
        elif choice == "5":
            try:
                rid = get_valid_int("Registration ID to delete:")
                Registration.delete_by_id(rid, db)
                print("Registration deleted successfully.")
            except Exception as e:
                print(f"Could not delete registration: {e}")
 
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
 
 
# =============================================================
# MAIN
# =============================================================
 
def main():
    print_header()
    try:
        db = Database()
    except ConnectionError as e:
        print(f"Could not connect to the database: {e}")
        return
 
    while True:
        print("\n--- Main Menu ---")
        print("1. Manage Students")
        print("2. Manage Teachers")
        print("3. Manage Courses")
        print("4. Manage Registrations")
        print("0. Exit")
        choice = input("Your choice: ").strip()
 
        if choice == "1":
            student_menu(db)
        elif choice == "2":
            teacher_menu(db)
        elif choice == "3":
            course_menu(db)
        elif choice == "4":
            registration_menu(db)
        elif choice == "0":
            db.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
 
 
if __name__ == "__main__":
    main()
