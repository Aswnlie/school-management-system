# =============================================================
# person.py
# Base class for Student and Teacher.
# Defines shared attributes: first name, last name, email, phone.
# Uses properties with validation (encapsulation).
# =============================================================


class Person:
    """
    Abstract base class representing a person in the school system.
    Shared by Student and Teacher via inheritance.
    """

    def __init__(self, first_name, last_name, email, phone=None):
        # Use setters so validation runs on construction too
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.phone      = phone

    # --- first_name ---

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not value.strip():
            raise ValueError("First name cannot be empty.")
        self._first_name = value.strip()

    # --- last_name ---

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not value.strip():
            raise ValueError("Last name cannot be empty.")
        self._last_name = value.strip()

    # --- email ---

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not value.strip():
            raise ValueError("Email cannot be empty.")
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email address.")
        self._email = value.strip()

    # --- phone ---

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if value:
            # Strip all allowed formatting characters before checking digits
            # Allows formats like: 555-1001, +7 701 234 56 78, (555) 123-4567
            cleaned = value.strip().replace("-", "").replace(" ", "").replace("+", "").replace("(", "").replace(")", "")
            if not cleaned.isdigit():
                raise ValueError("Phone number must contain only digits, spaces, dashes, or +.")
        self._phone = value.strip() if value else None

    # --- helpers ---

    def full_name(self):
        """Return the person's full name as 'First Last'."""
        return f"{self._first_name} {self._last_name}"

    def __str__(self):
        phone_text = self._phone if self._phone else "Not provided"
        return f"{self.full_name()} | {self._email} | {phone_text}"