import os


# The application reads this setting at import time to select its in-memory
# SQLite database instead of attempting to connect to local MySQL.
os.environ["TESTING"] = "true"
