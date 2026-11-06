# =============================================================
# teacher.py
# Teacher class — inherits from Person.
# Contains all CRUD operations for the Teachers table,
# called via MySQL stored procedures.
# =============================================================
 
from person import Person
 
 
class Teacher(Person):
    """
    Represents a teacher. Inherits shared person attributes from Person.
    Adds department and teacher_id specific to teachers.
    """
 
    def __init__(self, first_name, last_name, email, phone=None,
                 department=None, teacher_id=None):
        super().__init__(first_name, last_name, email, phone)
        self.teacher_id = teacher_id
        self.department = department
 
    # --- CRUD ---
 
    def add(self, db):
        """Insert this teacher into the database using the AddTeacher procedure."""
        db.call_proc("AddTeacher", [
            self._first_name,
            self._last_name,
            self._email,
            self._phone,
            self.department,
        ])
 
    def update(self, db):
        """Update this teacher's details using the UpdateTeacher procedure."""
        db.call_proc("UpdateTeacher", [
            self.teacher_id,
            self._first_name,
            self._last_name,
            self._email,
            self._phone,
            self.department,
        ])
 
    def delete(self, db):
        """Delete this teacher from the database using the DeleteTeacher procedure."""
        db.call_proc("DeleteTeacher", [self.teacher_id])
 
    # --- Static helpers ---
 
    @staticmethod
    def get_all(db):
        """Retrieve all teachers from the database, ordered by last name."""
        return db.call_proc("GetAllTeachers")
 
    @staticmethod
    def delete_by_id(teacher_id, db):
        """Delete a teacher by their ID using the DeleteTeacher procedure."""
        return db.call_proc("DeleteTeacher", [teacher_id])
 
    @staticmethod
    def search(term, db):
        """Search for teachers by ID, name, or department using the SearchTeacher procedure."""
        return db.call_proc("SearchTeacher", [term])
 
    @staticmethod
    def sort_by_name(rows):
        """
        Sort a list of teacher rows by last name, then first name.
        Columns: (TeacherID, FirstName, LastName, Email, Phone, Department)
                   index 0    index 1    index 2
        Uses Python's sorted() with a tuple key — O(n log n).
        """
        return sorted(rows, key=lambda row: (row[2].lower(), row[1].lower()))
 