import sqlite3

# Initial database file
DATABASE_FILE = 'DayOne.db'

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

def insert_employee(id, name, role, gender, contact, ClockInTime, ClockOutTime):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employees (id, name, role, gender, contact, ClockInTime, ClockOutTime) VALUES (?,?,?,?,?,?,?)",
                    (id, name, role, gender, contact, ClockInTime, ClockOutTime))
    conn.commit()
    conn.close()
    

create_table()

insert_employee('101', 'Parba', 'Barista', 'Male', '987654321', '2024-01-19 09:00:00', '2024-01-19 18:00:00')
insert_employee('102', 'Dimarucut', 'Waiter', 'Male', '987654322', '2024-01-19 09:00:00', '2024-01-19 12:00:00')
insert_employee('103', 'Menoc', 'Waiter', 'Male', '987654332', '2024-01-19 09:00:00', '2024-01-19 20:00:00')
insert_employee('104', 'Ashley', 'Cashier', 'Female', '987654432', '2024-01-19 10:00:00', '2024-01-19 18:00:00')
insert_employee('105', 'Esclamado', 'Chef', 'Male', '987654432', '2024-01-19 10:00:00', '2024-01-19 18:00:00')
