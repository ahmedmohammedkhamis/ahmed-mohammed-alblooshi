
# Import SQLite
import sqlite3

# Import time
import time

# Open database
conn = sqlite3.connect("tasks.db")

# Create cursor
cursor = conn.cursor()

# Get old status
cursor.execute("SELECT status FROM tasks WHERE id = 1")
old_status = cursor.fetchone()

# Check if task exists
if old_status:

    # Save old status
    old_status = old_status[0]

    # Change status to done
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = 1")

    # Save changes
    conn.commit()

    # Show new status
    print("Status changed to done")

    # Wait 15 seconds
    time.sleep(15)

    # Restore old status
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = 1",
        (old_status,)
    )

    # Save changes
    conn.commit()

    # Show old status
    print("Status restored to", old_status)

else:
    # Show error
    print("Task not found")

# Close database
conn.close()
