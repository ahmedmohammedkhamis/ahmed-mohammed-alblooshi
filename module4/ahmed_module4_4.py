
# Import SQLite
import sqlite3

# Open database
conn = sqlite3.connect("tasks.db")

# Create cursor
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# Show table names
print(cursor.fetchall())

# Get tasks data
cursor.execute("SELECT * FROM tasks")

# Show all rows
for row in cursor.fetchall():
    print(row)

# Close database
conn.close()
