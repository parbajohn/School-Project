import sqlite3

# Initial database file
DATABASE_FILE = 'Day One.db'

def update_connection(file_path):
    global DATABASE_FILE
    DATABASE_FILE = file_path

def create_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JanEmployees (
            unique_id TEXT PRIMARY KEY,
            employee_id TEXT,
            name TEXT,
            role TEXT,
            gender TEXT,
            contact TEXT,
            ClockInTime TEXT,
            ClockOutTime TEXT)''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MayEmployees (
            unique_id TEXT PRIMARY KEY,
            employee_id TEXT,
            name TEXT,
            role TEXT,
            gender TEXT,
            contact TEXT,
            ClockInTime TEXT,
            ClockOutTime TEXT)''')
    
    conn.commit()
    conn.close()

def generate_unique_id(employee_id, clock_in_time):
    # Use a combination of employee_id and clock_in_time as the unique_id
    return f"{employee_id}_{clock_in_time}"

def insert_employee(table, employee_id, name, role, gender, contact, ClockInTime, ClockOutTime):
    unique_id = generate_unique_id(employee_id, ClockInTime)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table} (unique_id, employee_id, name, role, gender, contact, ClockInTime, ClockOutTime) VALUES (?,?,?,?,?,?,?,?)",
                    (unique_id, employee_id, name, role, gender, contact, ClockInTime, ClockOutTime))
    conn.commit()
    conn.close()

def union_data():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Example query to union data from JanEmployees and MayEmployees tables
    cursor.execute('''
        SELECT unique_id, employee_id, name, ClockInTime, ClockOutTime
        FROM JanEmployees
        UNION
        SELECT unique_id, employee_id, name, ClockInTime, ClockOutTime
        FROM MayEmployees;
    ''')

    data = cursor.fetchall()
    conn.close()
    
    print("Fetched data:", data)  # Print the fetched data
    return data

create_tables()

# Insert data into JanEmployees table
insert_employee('JanEmployees', '101', 'Parba', 'Barista', 'Male', '987654321', '2024-01-19 09:00:00', '2024-01-19 18:00:00')
insert_employee('JanEmployees', '102', 'Dimarucut', 'Waiter', 'Male', '987654322', '2024-01-19 09:00:00', '2024-01-19 12:00:00')
insert_employee('JanEmployees', '103', 'Menoc', 'Waiter', 'Male', '987654332', '2024-01-19 09:00:00', '2024-01-19 20:00:00')
insert_employee('JanEmployees', '104', 'Ashley', 'Cashier', 'Female', '987654432', '2024-01-19 10:00:00', '2024-01-19 18:00:00')
insert_employee('JanEmployees', '105', 'Esclamado', 'Chef', 'Male', '987654432', '2024-01-19 10:00:00', '2024-01-19 18:00:00')

# Insert data into MayEmployees table
insert_employee('MayEmployees', '101', 'Parba', 'Barista', 'Male', '987654321', '2024-05-19 09:00:00', '2024-05-19 19:00:00')
insert_employee('MayEmployees', '102', 'Dimarucut', 'Waiter', 'Male', '987654322', '2024-05-19 09:00:00', '2024-05-19 16:00:00')
insert_employee('MayEmployees', '103', 'Menoc', 'Waiter', 'Male', '987654332', '2024-05-19 09:00:00', '2024-05-19 12:00:00')
insert_employee('MayEmployees', '104', 'Ashley', 'Cashier', 'Female', '987654432', '2024-05-19 10:00:00', '2024-05-19 15:00:00')
insert_employee('MayEmployees', '105', 'Esclamado', 'Chef', 'Male', '987654432', '2024-05-19 10:00:00', '2024-05-19 12:00:00')

union_data()
