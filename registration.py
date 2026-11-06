
# =============================================================
# registration.py
# Registration class — links Students and Courses.
# Provides CRUD operations via MySQL stored procedures.
# =============================================================


class Registration:
    """
    Represents a student's enrolment on a course.
    Acts as a junction between Students and Courses tables.
    Uses stored procedures for database operations.
    """

    def __init__(self, student_id=None, course_id=None,
                 registration_id=None, status="Enrolled",
                 registration_date=None):

        self.registration_id = registration_id
        self.student_id = student_id
        self.course_id = course_id
        self.status = status
        self.registration_date = registration_date

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def add(self, db):
        """
        Register a student on a course using AddRegistration procedure.
        """
        cursor = db.connection.cursor()
        cursor.callproc("AddRegistration", (
            self.student_id,
            self.course_id
        ))
        db.connection.commit()
        cursor.close()

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self, db):
        """
        Update registration details including student, course,
        registration date, and status.
        """
        if self.registration_id is None:
            raise ValueError("Registration ID is required for update.")

        cursor = db.connection.cursor()
        cursor.callproc("UpdateRegistration", (
            self.registration_id,
            self.student_id,
            self.course_id,
            self.registration_date,
            self.status
        ))
        db.connection.commit()
        cursor.close()

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(self, db):
        """
        Delete this registration using DeleteRegistration procedure.
        """
        if self.registration_id is None:
            raise ValueError("Registration ID is required for deletion.")

        cursor = db.connection.cursor()
        cursor.callproc("DeleteRegistration", (self.registration_id,))
        db.connection.commit()
        cursor.close()

    # ---------------------------------------------------------
    # STATIC METHODS
    # ---------------------------------------------------------

    @staticmethod
    def get_all(db):
        """
        Retrieve all registrations using GetAllRegistrations procedure.
        """
        cursor = db.connection.cursor()
        cursor.callproc("GetAllRegistrations")

        results = []
        for result in cursor.stored_results():
            results = result.fetchall()

        cursor.close()
        return results

    @staticmethod
    def search(term, db):
        """
        Search registrations by ID, student name, or course name.
        """
        cursor = db.connection.cursor()
        cursor.callproc("SearchRegistration", (term,))

        results = []
        for result in cursor.stored_results():
            results = result.fetchall()

        cursor.close()
        return results

    @staticmethod
    def delete_by_id(registration_id, db):
        """
        Delete a registration by ID.
        """
        cursor = db.connection.cursor()
        cursor.callproc("DeleteRegistration", (registration_id,))
        db.connection.commit()
        cursor.close()

    @staticmethod
    def sort_by_date(rows):
        """
        Sort registrations by date (descending order).

        Expected row structure:
        (RegistrationID, StudentName, CourseName, RegistrationDate, Status)
        """
        return sorted(rows, key=lambda row: row[3], reverse=True)
