# =============================================================
# student.py
# Student class — inherits from Person.
# Contains all CRUD operations for the Students table,
# called via MySQL stored procedures.
# =============================================================
 
from person import Person
 
 
class Student(Person):
    """
    Represents a student. Inherits shared person attributes from Person.
    Adds date_of_birth and student_id specific to students.
    """
 
    def __init__(self, first_name, last_name, email, phone=None,
                 date_of_birth=None, student_id=None, status="Active"):
        super().__init__(first_name, last_name, email, phone)
        self.student_id    = student_id
        self.date_of_birth = date_of_birth
        self.status        = status   # Active | Inactive | Graduated
 
    # --- CRUD ---
 
    def add(self, db):
        """Insert this student into the database using the AddStudent procedure."""
        db.call_proc("AddStudent", [
            self._first_name,
            self._last_name,
            self._email,
            self._phone,
            self.date_of_birth,
        ])
 
    def update(self, db):
        """Update this student's details using the UpdateStudent procedure.
        Includes DateOfBirth and Status so all fields can be changed."""
        db.call_proc("UpdateStudent", [
            self.student_id,
            self._first_name,
            self._last_name,
            self._email,
            self._phone,
            self.date_of_birth,
            self.status,
        ])
 
    def delete(self, db):
        """Delete this student from the database using the DeleteStudent procedure."""
        db.call_proc("DeleteStudent", [self.student_id])
 
    # --- Static helpers ---
 
    @staticmethod
    def get_all(db):
        """Retrieve all students from the database, ordered by last name."""
        return db.call_proc("GetAllStudents")
 
    @staticmethod
    def delete_by_id(student_id, db):
        """Delete a student by their ID using the DeleteStudent procedure."""
        return db.call_proc("DeleteStudent", [student_id])
 
    @staticmethod
    def search(term, db):
        """Search for students by ID or name using the SearchStudent procedure."""
        return db.call_proc("SearchStudent", [term])
 
    @staticmethod
    def sort_by_name(rows):
        """
        Sort a list of student rows by last name, then first name.
        Columns: (StudentID, FirstName, LastName, Email, Phone, DOB, Status)
                   index 0     index 1    index 2
        Uses Python's sorted() with a tuple key — O(n log n).
        """
        return sorted(rows, key=lambda row: (row[2].lower(), row[1].lower()))