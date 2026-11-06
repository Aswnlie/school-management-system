# =============================================================
# database.py
# Handles the MySQL connection for the entire application.
# All other classes import this to get the cursor and connection.
# =============================================================
import mysql.connector
from mysql.connector import Error
 
from config import DB_CONFIG
 
 
class Database:
    """
    Manages the connection to the MySQL SchoolManagementDB database.
    Database() is used to get a connection, then passed into all classes.
    """
 
    def __init__(self, config=None):
        self.config     = config if config is not None else DB_CONFIG
        self.connection = None
        self.connect()
 
    def connect(self):
        """Establish connection to MySQL on startup."""
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Database connected successfully.")
        except Error as err:
            print(f"Failed to connect to MySQL: {err}")
            raise ConnectionError(f"Failed to connect to database: {err}")
 
    def close(self):
        """Close database connection cleanly."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
 
    def call_proc(self, proc_name, params=()):
        """
        Execute a stored procedure and return ALL result rows.
 
        Uses cursor.callproc() which works on all mysql-connector-python
        versions without needing multi=True.
 
        Arguments:
            proc_name : Name of the stored procedure e.g. 'GetAllStudents'
            params    : Tuple or list of parameters to pass in
 
        Returns:
            A list of result rows (each row is a tuple).
            Returns an empty list if no rows or on error.
        """
        cursor = self.connection.cursor()
        try:
            # callproc() is the standard cross-version way to call procedures.
            # stored_results() then iterates over each result set returned.
            cursor.callproc(proc_name, list(params))
 
            results = []
            for result_set in cursor.stored_results():
                rows = result_set.fetchall()
                if rows:
                    results.extend(rows)
 
            self.connection.commit()
            return results
 
        except Exception as err:
            self.connection.rollback()
            raise RuntimeError(f"Error executing '{proc_name}': {err}") from err
        finally:
            cursor.close()
 
    def execute_query(self, query, params=()):
        """
        Execute a raw SQL query directly (not via stored procedure).
 
        Arguments:
            query  : SQL string e.g. "SELECT * FROM Students WHERE StudentID = %s"
            params : Tuple of parameters
 
        Returns:
            A list of rows.
        """
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as err:
            print(f"Query error: {err}")
            raise
        finally:
            cursor.close()
 
 
if __name__ == "__main__":
    db = Database()
    print("Database module loaded successfully.")
    db.close()
