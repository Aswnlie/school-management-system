# =============================================================
# course.py
# Course class — no parent class (courses are not persons).
# Contains all CRUD operations for the Courses table,
# called via MySQL stored procedures.
# =============================================================
 
 
class Course:
    """
    Represents a course in the school system.
    Handles all CRUD operations for the Courses table via stored procedures.
    """
 
    def __init__(self, course_name, description=None, credits=1,
                 teacher_id=None, course_id=None):
        self.course_id   = course_id
        self.course_name = course_name
        self.description = description
        self.credits     = credits
        self.teacher_id  = teacher_id
 
    # --- CRUD ---
 
    def add(self, db):
        """Insert this course into the database using the AddCourse procedure."""
        db.call_proc("AddCourse", [
            self.course_name,
            self.description,
            self.credits,
            self.teacher_id,
        ])
 
    def update(self, db):
        """Update this course's details using the UpdateCourse procedure."""
        db.call_proc("UpdateCourse", [
            self.course_id,
            self.course_name,
            self.description,
            self.credits,
            self.teacher_id,
        ])
 
    def delete(self, db):
        """Delete this course from the database using the DeleteCourse procedure."""
        db.call_proc("DeleteCourse", [self.course_id])
 
    # --- Static helpers ---
 
    @staticmethod
    def get_all(db):
        """Retrieve all courses from the database, with teacher names via JOIN."""
        return db.call_proc("GetAllCourses")
 
    @staticmethod
    def delete_by_id(course_id, db):
        """Delete a course by its ID using the DeleteCourse procedure."""
        return db.call_proc("DeleteCourse", [course_id])
 
    @staticmethod
    def search(term, db):
        """Search for courses by ID or name using the SearchCourse procedure."""
        return db.call_proc("SearchCourse", [term])
 
    @staticmethod
    def sort_by_name(rows):
        """
        Sort a list of course rows alphabetically by course name.
        Columns: (CourseID, CourseName, Description, Credits, TeacherName)
                   index 0   index 1
        Uses Python's sorted() with a string key — O(n log n).
        """
        return sorted(rows, key=lambda row: row[1].lower())
 