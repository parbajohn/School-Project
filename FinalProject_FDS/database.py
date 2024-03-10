import sqlite3

# Initial database file
DATABASE_FILE = 'DayOne'

def update_connection(file_path):
    global DATABASE_FILE
    DATABASE_FILE = file_path

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            gender TEXT,
            contact TEXT,
            ClockInTime TEXT,
            ClockOutTime TEXT)''')
    conn.commit()
    conn.close()

def fetch_employees():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Employees')
    employees = cursor.fetchall()
    conn.close()
    return employees

def insert_employee(id, name, role, gender, contact, ClockInTime, ClockOutTime):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employees (id, name, role, gender, contact, ClockInTime, ClockOutTime) VALUES (?,?,?,?,?,?,?)",
                    (id, name, role, gender, contact, ClockInTime, ClockOutTime))
    conn.commit()
    conn.close()

def delete_employee(id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE from Employees WHERE id=?", (id, ))
    conn.commit()
    conn.close()

def update_employee(new_name, new_role, new_gender, new_contact, new_ClockInTime, new_ClockOutTime, id):
    print("Updating employee:", id, new_name, new_role, new_gender, new_contact, new_ClockInTime, new_ClockOutTime)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Employees SET name=?, role=?, gender=?, contact=?, ClockInTime=?, ClockOutTime=? WHERE id=?",
        (new_name, new_role, new_gender, new_contact, new_ClockInTime, new_ClockOutTime, id)
    )
    conn.commit()
    conn.close()

def id_exists(id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Employees WHERE id=?", (id,))
    count = cursor.fetchone()
    conn.close()
    return count[0] > 0

def get_employee_id(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Employees WHERE name=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def fetch_employee_by_id(employee_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Employees WHERE id=?', (employee_id,))
    employee_data = cursor.fetchone()
    conn.close()

    if employee_data:
        # Convert the tuple to a dictionary
        return {
            'ID': employee_data[0],
            'Name': employee_data[1],
            'Role': employee_data[2],
            'Gender': employee_data[3],
            'Contact': employee_data[4],
            'ClockInTime': employee_data[5],
            'ClockOutTime': employee_data[6]
        }
    else:
        return None

def update_clock_in_time(employee_id, current_time):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Employees SET ClockInTime=? WHERE id=?", (current_time, employee_id))
    conn.commit()
    conn.close()

def update_clock_out_time(employee_id, clock_out_time):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Employees SET ClockOutTime=? WHERE id=?", (clock_out_time, employee_id))
    conn.commit()
    conn.close()

def update_connection(selected_db):
    global DATABASE_FILE
    DATABASE_FILE = selected_db
 

create_table()
