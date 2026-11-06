# =============================================================
# config.example.py
# Template for the database connection settings.
#
# HOW TO USE:
#   1. Copy this file and name the copy  config.py
#   2. Replace the placeholder values below with your own MySQL details
#   3. Never commit config.py (it is listed in .gitignore)
# =============================================================

DB_CONFIG = {
    "host":       "localhost",
    "user":       "root",                  # your MySQL username
    "password":   "your_password_here",    # your MySQL password
    "database":   "SchoolManagementDB",
    "charset":    "utf8mb4",
    "use_unicode": True,
}
