# COMP3005B Assignment 3 Q1: Database Interaction with PostgreSQL and Application Programming

Implements a PostgreSQL database using the provided schema and a Python app that connects to this database to perform specific CRUD (Create, Read, Update, Delete) operations.

## Database Schema

The database contains a single table named `students`:

| Column          | Type    | Constraints                |
|-----------------|---------|----------------------------|
| student_id      | Integer | Primary Key, Auto-increment |
| first_name      | Text    | Not Null                   |
| last_name       | Text    | Not Null                   |
| email           | Text    | Not Null, Unique           |
| enrollment_date | Date    | Optional                   |

Initial data:

```sql
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim',  'Beam',  'jim.beam@example.com',  '2023-09-02');
```

The above SQL schema is created in init.sql.

## Requirements

PostgreSQL installed and running (default port: 5432, default user: postsgres)

Python 3.10+ installed

This Python package:

```bash
pip install "psycopg[binary]==3.2.*"
```

## Installation

1. Clone the project and navigate into it:
```bash
git clone https://github.com/dennisc3000/COMP3005B-A3-Q1.git
cd COMP3005B-A3-Q1
```

2. Install the Python PostgresSQL driver:
```bash
pip install "psycopg[binary]==3.2.*"
```

## Usage

1. Create the database
In pgAdmin: 
```sql
CREATE DATABASE studentdb;
```

2. Run the script
```sql
\i init.sql
```

3. Configure environment variables *and make sure these commands are entered one by one*
```bash
set PGHOST=localhost
set PGPORT=5432
set PGDATABASE=studentdb
set PGUSER=postgres
set PGPASSWORD=**your_password_here**
```

4. Test to ensure environment variables are set correctly
```bash
python -c "import psycopg; psycopg.connect() and print('Connection successful!')"
```

5. Run the CRUD app *from the same CLI window that you set the environment variables in because they need to be set every time the app is run.*

________________________________________________

Show the database's current state:
  ```bash
  py app.py list
  ```

Add a new student to the database:
```bash
py app.py add "Rachel" "Waring" "rachelwaring@example.com" 2025-09-01
```

Update an existing student's email (need to know their student ID):
```bash
py app.py update 4 "rachelwaring317@example.com"
```

Delete a student from the database (need to know their student ID):
```bash
py app.py delete 4
```

Run a demo of a full CRUD cycle:
  ```bash
  py app.py
  ```

  The demo does the following:
  
  Read: Displays current state.
  
  Create: Creates a sample student: Rachel Waring, email: rachelwaring@example.com, enrolment date: 2025-09-01.
  
  Update: Updates that student's email to rachelwaring317@example.com.
  
  Delete: Deletes that student from the database.
  
  Read: Displays final state.

