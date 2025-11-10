# app.py
# Purpose:
#   Connect to PostgreSQL using psycopg3 and implement 4 CRUD functions:
#   - getAllStudents()
#   - addStudent(first_name, last_name, email, enrollment_date)
#   - updateStudentEmail(student_id, new_email)
#   - deleteStudent(student_id)
#
# How it connects:
#   Uses standard PG* environment variables that should be set up in this CMD window:
#   PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
#
# How to run:
#   py app.py list
#   py app.py add "Rachel" "Waring" "rachelwaring@example.com" 2025-09-01
#   py app.py update 1 "john.new@example.com"
#   py app.py delete 1
#   py app.py        # runs a small demo (add/update/delete) against the DB

from __future__ import annotations
from typing import List, Dict, Optional
import psycopg
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation



# Connection factory
# Encapsulates creating a DB connection. psycopg will read PG* env vars.
def _connect():
    # row_factory=dict_row makes fetches return dicts instead of tuples
    return psycopg.connect(row_factory=dict_row)



# CRUD functions

def getAllStudents() -> List[Dict]:
    """Read: return all rows as a list of dicts."""
    sql = """
        SELECT student_id, first_name, last_name, email, enrollment_date
        FROM students
        ORDER BY student_id
    """
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()



def addStudent(first_name: str, last_name: str,
               email: str, enrollment_date: Optional[str]) -> int:
    """
    Create: insert a student. enrollment_date is 'YYYY-MM-DD' or None
    Returns the new student_id
    Raises ValueError if email violates the UNIQUE constraint
    """
    sql = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id
    """
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (first_name, last_name, email, enrollment_date))
            new_id = cur.fetchone()["student_id"]
            conn.commit()  # persist the insert
            return new_id
    except UniqueViolation:
        # Convert DB error to a clean Python exception
        raise ValueError(f"Email already exists: {email}")



def updateStudentEmail(student_id: int, new_email: str) -> bool:
    """
    Update: set a new email for a given student_id
    Returns True if exactly one row was updated, False if student_id not found.
    Raises ValueError if new_email violates the UNIQUE constraint.
    """
    sql = "UPDATE students SET email = %s WHERE student_id = %s"
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (new_email, student_id))
            changed = cur.rowcount == 1  # rowcount is number of affected rows
            conn.commit()
            return changed
    except UniqueViolation:
        raise ValueError(f"Email already exists: {new_email}")



def deleteStudent(student_id: int) -> bool:
    """
    Delete: remove the student with the given id
    Returns True if one row was deleted, False if that student doesn't exist
    """
    sql = "DELETE FROM students WHERE student_id = %s"
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (student_id,))
        deleted = cur.rowcount == 1
        conn.commit()
        return deleted




# Simple CLI and demo runner
# Test functions from Windows Command Prompt
if __name__ == "__main__":
    import sys


    # If no args, run a tiny demo flow (list -> add -> update -> delete -> list)
    if len(sys.argv) == 1:
        print("Initial rows:")
        for s in getAllStudents():
            print(f"ID: {s['student_id']}, Name: {s['first_name']} {s['last_name']}, "
                f"Email: {s['email']}, Enrollment Date: {s['enrollment_date']}")

        # --- Create ---
        first, last = "Rachel", "Waring"
        email = "rachelwaring@example.com"
        date = "2025-09-01"
        print(f"\nAdding a sample student: {first} {last} ...")
        sid = addStudent(first, last, email, date)
        print(f"Added student:\n  ID: {sid}, Name: {first} {last}, "
            f"Email: {email}, Enrollment Date: {date}")

        # --- Update ---
        new_email = "rachelwaring317@example.com"
        print(f"\nUpdating {first} {last}'s email to '{new_email}' ...")
        updateStudentEmail(sid, new_email)
        student = [s for s in getAllStudents() if s["student_id"] == sid][0]
        print(f"After update:\n  ID: {student['student_id']}, Name: {student['first_name']} {student['last_name']}, "
            f"Email: {student['email']}, Enrollment Date: {student['enrollment_date']}")

        # --- Delete ---
        print(f"\nDeleting {first} {last} ...")
        deleteStudent(sid)

        print("Final rows:")
        for s in getAllStudents():
            print(f"ID: {s['student_id']}, Name: {s['first_name']} {s['last_name']}, "
                f"Email: {s['email']}, Enrollment Date: {s['enrollment_date']}")
        sys.exit(0)





    # Subcommands: list | add | update | delete
    cmd = sys.argv[1].lower()

    if cmd == "list":
        for row in getAllStudents():
            print(row)

    elif cmd == "add":
        # Usage: py app.py add FIRST LAST EMAIL YYYY-MM-DD|NULL
        if len(sys.argv) < 6:
            print('Usage: py app.py add FIRST LAST EMAIL YYYY-MM-DD|NULL')
            sys.exit(1)
        first, last, email, date_str = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        date_val = None if date_str.upper() == "NULL" else date_str
        try:
            new_id = addStudent(first, last, email, date_val)
            print(f"Inserted student_id={new_id}")
        except ValueError as e:
            print(f"Error: {e}")

    elif cmd == "update":
        # Usage: py app.py update STUDENT_ID NEW_EMAIL
        if len(sys.argv) < 4:
            print('Usage: py app.py update STUDENT_ID NEW_EMAIL')
            sys.exit(1)
        sid = int(sys.argv[2]); new_email = sys.argv[3]
        try:
            ok = updateStudentEmail(sid, new_email)
            print("Updated" if ok else "No such student_id")
        except ValueError as e:
            print(f"Error: {e}")

    elif cmd == "delete":
        # Usage: py app.py delete STUDENT_ID
        if len(sys.argv) < 3:
            print('Usage: py app.py delete STUDENT_ID')
            sys.exit(1)
        sid = int(sys.argv[2])
        ok = deleteStudent(sid)
        print("Deleted" if ok else "No such student_id")

    else:
        print("Unknown command. Use: list | add | update | delete")
        sys.exit(1)
