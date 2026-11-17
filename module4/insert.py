
# Import FastAPI
from fastapi import FastAPI

# Import SQLite
import sqlite3

# Create the app
app = FastAPI()

# Create POST API
@app.post("/insert")
def insert_tasks():

    # Open the database
    conn = sqlite3.connect("tasks.db")

    # Create cursor
    cursor = conn.cursor()

    # Add first task
    cursor.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
    """, ("Study Python", "Learn Python", "pending"))

    # Add second task
    cursor.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
    """, ("Study SQL", "Learn SQL", "pending"))

    # Save data
    conn.commit()

    # Close database
    conn.close()

    # Return message
    return {"message": "2 tasks added"}
