import sqlite3
import datetime


def log_operation(loginformation):
    with open("db_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {loginformation}\n")



try:
    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()
    print("Database connected successfully")
    log_operation("Database connected successfully.")
except sqlite3.Error as e:
    print(f"Database connection failed: {e}")
    log_operation(f"ERROR: Database connection failed - {e}")



def create_employee_table():
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            department TEXT
        )
        ''')
        conn.commit()
        print("Employee table created successfully.")
        log_operation("Employee table created successfully.")

        
        cursor.execute("DELETE FROM employees")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='employees'")
        conn.commit()
        print("Old records and ID counter cleared successfully.")
        log_operation("Old records and ID counter cleared successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        log_operation(f"ERROR: Failed to create or reset table - {e}")



def insert_employee(name, age, department):
    try:
        print(f"Inserting employee: {name}")
        cursor.execute('''
        INSERT INTO employees (name, age, department)
        VALUES (?, ?, ?)
        ''', (name, age, department))
        conn.commit()
        print("Employee data inserted successfully.")
        log_operation(f"Inserted employee: {name}, Age: {age}, Dept: {department}")
    except sqlite3.Error as e:
        print(f"Error inserting employee: {e}")
        log_operation(f"ERROR inserting employee ({name}) - {e}")



def fetch_all_employees():
    try:
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        print("\nAll Employee Records:")
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
        log_operation("Fetched all employee records.")
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")
        log_operation(f"ERROR fetching records - {e}")


def update_employee(emp_id, name=None, age=None, department=None):
    try:
        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)
        if age:
            updates.append("age = ?")
            params.append(age)
        if department:
            updates.append("department = ?")
            params.append(department)

        if not updates:
            print("No fields to update.")
            log_operation(f"No fields to update for employee ID {emp_id}.")
            return

        params.append(emp_id)
        query = f"UPDATE employees SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, tuple(params))
        conn.commit()
        print("Employee record updated successfully.")
        log_operation(f"Updated employee ID {emp_id} with fields {updates}.")
    except sqlite3.Error as e:
        print(f"Error updating record: {e}")
        log_operation(f"ERROR updating employee ID {emp_id} - {e}")



try:
    create_employee_table()

    insert_employee('Srinu Naidu', 22, 'HR')
    insert_employee('Ramesh', 23, 'Finance')
    insert_employee('Ajay', 22, 'Testing')

    print("\nBefore Updates:")
    fetch_all_employees()

    update_employee(2, "Pranay", 24, "Banking")

    print("\nAfter Updates:")
    fetch_all_employees()

    conn.close()
    print("\nDatabase connection closed.")
    log_operation("Database connection closed.")

except Exception as e:
    print(f"Unexpected error: {e}")
    log_operation(f"Unexpected error: {e}")
