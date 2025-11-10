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

PostgreSQL installed and running (default port 5432)

Python 3.10+ installed

This Python package:

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

3. Open Windows Command Prompt, install the Python PostgresSQL driver:
```bash
pip install "psycopg[binary]==3.2.*"
```

4. Configure environment variables in *and make sure these commands are entered one by one*
```bash
set PGHOST=localhost
set PGPORT=5432
set PGDATABASE=studentdb
set PGUSER=postgres
set PGPASSWORD=**your_password_here**
```

5. Run the CRUD app from the Windows CLI: list shows the database's current state. *Make sure you run from the same window as you set the environment variables because they need to be set every time the app is run.*
```bash
py app.py list
```

Run a demo of a full CRUD cycle. It does the following:
Displays current state. Add a sample student: Rachel Waring, email: rachelwaring@example.com, enrolment date: 2025-09-01. Update that student's email to rachelwaring317@example.com. Delete that student from database. Display final state.
```bash
py app.py
```
