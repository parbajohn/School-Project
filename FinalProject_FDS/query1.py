import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Database connection settings
DATABASE_FILE = 'DayOne.db'

def open_main_window():
    app = tk.Tk()
    app.title('Employee Management System')
    app.geometry('1200x600')
    app.config(bg='pink')
    app.resizable(False, False)

    font1 = ('Arial', 20, 'bold')
    font2 = ('Arial', 12, 'bold')

    style = ttk.Style(app)

    style.theme_use('clam')
    style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
    style.map('Treeview', background=[('selected', '#1A8F2D')])
    tree = ttk.Treeview(app, height=15)

    tree['columns'] = ('ID', 'Name', 'ClockInTime', 'ClockOutTime', 'TotalWorkingHours', 'OvertimeHours', 'Remarks')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', anchor=tk.CENTER, width=80)
    tree.column('Name', anchor=tk.W, width=120)
    tree.column('ClockInTime', anchor=tk.CENTER, width=120)
    tree.column('ClockOutTime', anchor=tk.CENTER, width=120)
    tree.column('TotalWorkingHours', anchor=tk.CENTER, width=120)
    tree.column('OvertimeHours', anchor=tk.CENTER, width=120)
    tree.column('Remarks', anchor=tk.W, width=120)

    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('ClockInTime', text='ClockInTime')
    tree.heading('ClockOutTime', text='ClockOutTime')
    tree.heading('TotalWorkingHours', text='Total Working Hours')
    tree.heading('OvertimeHours', text='OT')
    tree.heading('Remarks', text='Remarks')

    tree.place(x=100, y=20)
    tree.pack(fill='both', expand=True)

    # Fetch data from the database
    try:
        data = fetch_employees()
        for row in data:
            tree.insert('', 'end', values=row)
    except sqlite3.OperationalError as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

    app.mainloop()

# Function to fetch employee data from the database
def fetch_employees():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                ID, 
                Name, 
                ClockInTime, 
                ClockOutTime,
                CAST((strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 AS INTEGER) AS TotalWorkingHours,
                CASE
                    WHEN (strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 > 8 THEN
                        CAST((strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 - 8 AS INTEGER)
                    ELSE 0
                END AS OvertimeHours,
                CASE
                    WHEN (strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 < 8 THEN 'UT'
                    WHEN (strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 > 8 THEN 'OT'
                    ELSE 'RT'
                END AS Remarks
            FROM Employees;
        """)

        data = cursor.fetchall()
        conn.close()

        print("Fetched data:", data)  # Add this line to check if data is fetched successfully
        return data
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Creating tables if they don't exist
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            ID TEXT PRIMARY KEY,
            Name TEXT,
            ClockInTime DATETIME,
            ClockOutTime DATETIME
        )
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EmployeeManagement (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            ClockInTime DATETIME,
            ClockOutTime DATETIME,
            TotalWorkingHours INTEGER,
            OvertimeHours INTEGER,
            Remarks TEXT
        )
    """)
    conn.commit()
    # Open the main window
    open_main_window()

    # Close the connection
    conn.close()
