import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

DATABASE_FILE = 'Day One.db'

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

    tree['columns'] = ('Unique ID', 'ID', 'Name', 'Gender', 'Total Working Hours')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('Unique ID', anchor=tk.CENTER, width=150)
    tree.column('ID', anchor=tk.CENTER, width=80)
    tree.column('Name', anchor=tk.CENTER, width=120)
    tree.column('Gender', anchor=tk.CENTER, width=150)
    tree.column('Total Working Hours', anchor=tk.CENTER, width=150)
    
    tree.heading('Unique ID', text='Unique ID')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Gender', text='Gender')
    tree.heading('Total Working Hours', text='Total Working Hours')

    tree.place(x=100, y=20)
    tree.pack(fill='both', expand=True)

    try:
        data = fetch_employees(order_by='TotalWorkingHours DESC')
        if data:
            for row in data:
                # Check if the format of unique_id is as expected
                if '_' in row[0]:
                    row[0] = row[0].split('_')[1].split()[0]
                tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("No Data", "No data to display.")
    except sqlite3.OperationalError as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

    app.mainloop()

def fetch_employees(order_by='TotalWorkingHours ASC'):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT 
                strftime('%Y-%m-%d', ClockInTime) AS unique_id,
                employee_id,
                name,
                gender,
                CAST((strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 AS INTEGER) AS TotalWorkingHours
            FROM JanEmployees
            UNION
            SELECT
                strftime('%Y-%m-%d', ClockInTime) AS unique_id,
                employee_id,
                name,
                gender,
                CAST((strftime('%s', ClockOutTime) - strftime('%s', ClockInTime)) / 3600.0 AS INTEGER) AS TotalWorkingHours
            FROM MayEmployees
            ORDER BY {order_by};
        """)

        data = cursor.fetchall()
        conn.close()

        print("Fetched data:", data)
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
    CREATE TABLE IF NOT EXISTS CombineEmployees (
        unique_id TEXT PRIMARY KEY,       
        employee_id TEXT,
        name TEXT,
        gender TEXT,
        ClockInTime DATETIME,
        ClockOutTime DATETIME,
        TotalWorkingHours INTEGER
    )
""")
conn.commit()

open_main_window()
