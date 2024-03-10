import customtkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
from datetime import datetime, time
from datetime import datetime, time as dt_time
import time

def resize_image(image_path, size):
    original_image = Image.open(image_path)
    resized_image = original_image.resize(size)
    return ImageTk.PhotoImage(resized_image)

def admin_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == 'a' and password == 'a':
        login_window.destroy()
        open_main_window()
    elif username == 'e' and password == 'e':
        login_window.destroy()
        open_employee1_window()
    else:
        messagebox.showerror('Login Failed', 'Invalid username or password')

def open_employee1_window():
    def start_working():
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current time in the required format

        # Define the time range for checking
        start_time = dt_time(9, 0)  # 9:00 AM

        if datetime.now().time() >= start_time:
            # Allow starting work only if it's beyond the start time
            # Update the database with the current time as ClockInTime
            employee_id = id_entry.get()  # Get the employee ID from the entry widget
            database.update_clock_in_time(employee_id, current_time)

            # Add your additional logic or actions here when starting work.

            messagebox.showinfo('Time Checker', 'You have started working.')
        else:
            messagebox.showwarning('Time Checker', 'It\'s not the required start working time. Cannot start working now.')

    def end_working():
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current time in the required format

        # Define the time range for checking
        start_time = dt_time(9, 0)  # 9:00 AM
        end_time = dt_time(19, 0)   # 5:00 PM

        if start_time <= datetime.now().time() <= end_time:
            # Update the database with the current time as ClockOutTime
            employee_id = id_entry.get()  # Get the employee ID from the entry widget
            database.update_clock_out_time(employee_id, current_time)

            # Add your additional logic or actions here when ending work.

            messagebox.showinfo('Time Checker', 'You have ended working.')
        else:
            messagebox.showwarning('Time Checker', 'It\'s not end working hours. Cannot end working now.')
   
    def search_employee():
        entered_id = id_entry.get()
        if entered_id:
            employee_data = database.fetch_employee_by_id(entered_id)
            if employee_data:
                update_employee_details(employee_data)
            else:
                messagebox.showerror('Error', 'Employee not found with ID: {}'.format(entered_id))
        else:
            messagebox.showwarning('Warning', 'Please enter an employee ID to search.')

    def update_employee_details(data):
        name_entry.delete(0, END)
        role_entry.delete(0, END)
        gender_entry.delete(0, END)
        contact_entry.delete(0, END)

        name_entry.insert(0, data['Name'])
        role_entry.insert(0, data['Role'])
        gender_entry.insert(0, data['Gender'])
        contact_entry.insert(0, data['Contact'])

    tree = ttk.Treeview

    def add_to_treeview():
        employees = database.fetch_employees()
        tree.delete(*tree.get_children())
        for employee in employees:
            tree.insert('', END, values=employee)

    def choose_database_file():
        selected_db = selected_db_var.get()
        if selected_db:
            database.update_connection(selected_db)
            add_to_treeview()
        else:
            messagebox.showerror('Error', 'Please choose a database file.')

    app = customtkinter.CTk()
    app.title('Employee Attendance System')
    app.geometry('1200x600')
    app.config(bg='lightblue')  # You can change the background color
    app.resizable(False, False)

    sticker_size = (180, 180)
    sticker_photo = resize_image('logo.jpg', sticker_size)
    sticker_label = Label(app, image=sticker_photo)
    sticker_label.place(x=900, y=200)

    database_files = ['Day1']

    selected_db_var = StringVar()


    id_label = customtkinter.CTkLabel(app, font=('Arial', 16), text='ID:', text_color='#000', bg_color='lightblue')
    id_label.place(x=20, y=50) 
    
    id_entry = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    id_entry.place(x=100, y=50)

    search_button = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='Search',
                                            fg_color='#05A321', hover_color='#00850B', bg_color='lightblue',
                                            cursor='hand2', corner_radius=15, width=120, command=search_employee)
    search_button.place(x=300, y=50)

    name_label = customtkinter.CTkLabel(app, font=('Arial', 16), text='Name:', text_color='#000', bg_color='lightblue')
    name_label.place(x=20, y=120)

    name_entry = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    name_entry.place(x=100, y=120)

    role_label = customtkinter.CTkLabel(app, font=('Arial', 16), text='Role:', text_color='#000', bg_color='lightblue')
    role_label.place(x=20, y=170)

    role_entry = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    role_entry.place(x=100, y=170)

    gender_label = customtkinter.CTkLabel(app, font=('Arial', 16), text='Gender:', text_color='#000', bg_color='lightblue')
    gender_label.place(x=20, y=220)

    gender_entry = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    gender_entry.place(x=100, y=220)

    contact_label = customtkinter.CTkLabel(app, font=('Arial', 16), text='Contact:', text_color='#000', bg_color='lightblue')
    contact_label.place(x=20, y=270)

    contact_entry = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    contact_entry.place(x=100, y=270)

    start_button = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='Start Working',
                                         fg_color='#05A321', hover_color='#00850B', bg_color='lightblue', cursor='hand2',
                                         corner_radius=15, width=260, command=start_working)
    start_button.place(x=860, y=400)

    end_button = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='End Work',
                                         fg_color='#05A321', hover_color='#00850B', bg_color='lightblue', cursor='hand2',
                                         corner_radius=15, width=260, command=end_working)
    end_button.place(x=860, y=450)

    db_options = customtkinter.CTkComboBox(app, font=('Arial', 16), text_color='#000', fg_color='#fff',
                                            dropdown_hover_color='#0C9295', button_color='#0C9295',
                                            button_hover_color='#0C9295', border_color='#0C9295', width=270,
                                            variable=selected_db_var, values=database_files, state='readonly')
    db_options.set('Choose Day')
    db_options.place(x=28, y=550)

    update_table_button = customtkinter.CTkButton(app, command=choose_database_file, font=('Arial', 16), text_color='#fff',
                                              text='Choose Day', fg_color='#05A321', hover_color='#00850B',
                                              bg_color='lightblue', cursor='hand2', corner_radius=15, width=260)
    update_table_button.place(x=300, y=550)

    app.mainloop()



def calculate_working_hours(clock_in_time, clock_out_time):
    if clock_in_time and clock_out_time:
        clock_in = datetime.strptime(clock_in_time, "%Y-%m-%d %H:%M:%S")
        clock_out = datetime.strptime(clock_out_time, "%Y-%m-%d %H:%M:%S")
        working_hours = (clock_out - clock_in).total_seconds() / 3600.0
        return round(working_hours, 2)
    else:
        return 0.0

def payroll_window():
    app = customtkinter.CTk()
    app.title('Employee Management System')
    app.geometry('1200x600')
    app.config(bg='lightblue')
    app.resizable(False, False)

    def search_employee():
        entered_id = id_entry.get()
        if entered_id:
            employee_data = database.fetch_employee_by_id(entered_id)
            if employee_data:
                update_employee_details(employee_data)
                update_working_hours_and_salary(employee_data)
            else:
                messagebox.showerror('Error', 'Employee not found with ID: {}'.format(entered_id))
        else:
            messagebox.showwarning('Warning', 'Please enter an employee ID to search.')

    def update_working_hours_and_salary(employee_data):
        clock_in_time = employee_data['ClockInTime']
        clock_out_time = employee_data['ClockOutTime']

        working_hours = calculate_working_hours(clock_in_time, clock_out_time)
        pay_rate = 45.0
        salary = round(working_hours * pay_rate, 2)

        working_hours_entry.delete(0, END)
        working_hours_entry.insert(0, str(working_hours))

        pay_entry.delete(0, END)
        pay_entry.insert(0, '₱' + str(salary))

    def update_employee_details(data):
        name_entry.delete(0, END)
        role_entry.delete(0, END)
        gender_entry.delete(0, END)
        contact_entry.delete(0, END)

        name_entry.insert(0, data['Name'])
        role_entry.insert(0, data['Role'])
        gender_entry.insert(0, data['Gender'])
        contact_entry.insert(0, data['Contact'])

    id_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='ID:', text_color='#fff', bg_color='lightblue')
    id_label.place(x=100, y=50)

    id_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    id_entry.place(x=240, y=50)

    search_button = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='Search',
                                            fg_color='#05A321', hover_color='#00850B', bg_color='lightblue',
                                            cursor='hand2', corner_radius=15, width=120, command=search_employee)
    search_button.place(x=450, y=50)

    name_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='Name:', text_color='#fff', bg_color='lightblue')
    name_label.place(x=100, y=100)

    name_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    name_entry.place(x=240, y=100)

    role_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='Role:', text_color='#fff', bg_color='lightblue')
    role_label.place(x=100, y=150)

    role_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    role_entry.place(x=240, y=150)

    gender_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='Gender:', text_color='#fff', bg_color='lightblue')
    gender_label.place(x=100, y=200)

    gender_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    gender_entry.place(x=240, y=200)

    contact_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='Contact Info.:', text_color='#fff', bg_color='lightblue')
    contact_label.place(x=100, y=250)

    contact_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    contact_entry.place(x=240, y=250)

    working_hours_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='Working Hours:', text_color='#fff', bg_color='lightblue')
    working_hours_label.place(x=100, y=300)

    working_hours_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    working_hours_entry.place(x=240, y=300)

    pay_label = customtkinter.CTkLabel(app, font=('Arial', 20, 'bold'), text='Salary:', text_color='#fff', bg_color='lightblue')
    pay_label.place(x=100, y=350)

    pay_entry = customtkinter.CTkEntry(app, font=('Arial', 20, 'bold'), text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    pay_entry.place(x=240, y=350)
    
    app.mainloop()

def open_main_window():
    global sticker_photo
    app = customtkinter.CTk()
    app.title('Employee Management System')
    app.geometry('1200x600')
    app.config(bg='pink')
    app.resizable(False, False)
    
    sticker_size = (400, 180)
    sticker_photo = resize_image('logo.jpg', sticker_size)
    sticker_label = Label(app, image=sticker_photo)
    sticker_label.place(x=1000, y=550)

    font1 = ('Arial', 20, 'bold')
    font2 = ('Arial', 12, 'bold')

    database_files = ['Day1']

    selected_db_var = StringVar()

    def add_to_treeview():
        employees = database.fetch_employees()
        tree.delete(*tree.get_children())
        for employee in employees:
            tree.insert('', END, values=employee)

    def clear(*clicked):
        if clicked:
            tree.selection_remove(tree.focus())
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        role_entry.delete(0, END)
        variable1.set('Choose one')
        contact_entry.delete(0, END)
        ClockInTime_entry.delete(0, END)
        ClockOutTime_entry.delete(0, END)

    def display_data(event):
        selected_item = tree.focus()
        if selected_item:
            row = tree.item(selected_item)['values']
            clear()
            id_entry.insert(0, row[0])
            name_entry.insert(0, row[1])
            role_entry.insert(0, row[2])
            variable1.set(row[3])
            contact_entry.insert(0, row[4])
            ClockInTime_entry.insert(0, row[5])
            ClockOutTime_entry.insert(0, row[6])
        else:
            pass

    def delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to delete.')
        else:
            id = id_entry.get()
        if id:
            if database.id_exists(id):
                database.delete_employee(id)
                add_to_treeview()
                clear()
            else:
                messagebox.showerror('Error', 'Invalid ID')
        else:
            messagebox.showerror('Error', 'ID is required for delete.')

    def update():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to update.')
        else:
            id = id_entry.get()
        if id:
            if database.id_exists(id):
                name = name_entry.get()
                role = role_entry.get()
                gender = variable1.get()
                contact = contact_entry.get()
                ClockInTime = ClockInTime_entry.get()
                ClockOutTime = ClockOutTime_entry.get()
                database.update_employee(name, role, gender, contact, ClockInTime, ClockOutTime, id)
                add_to_treeview()
                clear()
            else:
                messagebox.showerror('Error', 'Invalid ID')
        else:
            messagebox.showerror('Error', 'ID is required for update.')

    def insert():
        id = id_entry.get()
        name = name_entry.get()
        role = role_entry.get()
        gender = variable1.get()
        contact = contact_entry.get()
        ClockInTime = ClockInTime_entry.get()
        ClockOutTime = ClockOutTime_entry.get()
        if not (id and name and role and gender and contact):
            messagebox.showerror("Error", "Enter all fields.")
        elif database.id_exists(id):
            messagebox.showerror("Error", "ID already exists.")
        else:
            database.insert_employee(id, name, role, gender, contact, ClockInTime, ClockOutTime)
            add_to_treeview()

    def choose_database_file():
        selected_db = selected_db_var.get()
        if selected_db:
            database.update_connection(selected_db)
            add_to_treeview()
        else:
            messagebox.showerror('Error', 'Please choose a database file.')

    id_label = customtkinter.CTkLabel(app, font=font1, text='ID:', text_color='#fff', bg_color='pink')
    id_label.place(x=20, y=20)

    id_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                       border_width=2, width=180)
    id_entry.place(x=100, y=20)

    name_label = customtkinter.CTkLabel(app, font=font1, text='Name:', text_color='#fff', bg_color='pink')
    name_label.place(x=20, y=80)

    name_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                         border_width=2, width=180)
    name_entry.place(x=100, y=80)

    role_label = customtkinter.CTkLabel(app, font=font1, text='Role:', text_color='#fff', bg_color='pink')
    role_label.place(x=20, y=140)

    role_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                          border_width=2, width=180)
    role_entry.place(x=100, y=140)

    gender_label = customtkinter.CTkLabel(app, font=font1, text='Gender:', text_color='#fff', bg_color='pink')
    gender_label.place(x=20, y=200)

    options = ['Male', 'Female']
    variable1 = StringVar()

    gender_options = customtkinter.CTkComboBox(app, font=font1, text_color='#000', fg_color='#fff',
                                                dropdown_hover_color='#0C9295', button_color='#0C9295',
                                                button_hover_color='#0C9295', border_color='#0C9295', width=180,
                                                variable=variable1, values=options, state='readonly')
    gender_options.set('Choose one')
    gender_options.place(x=100, y=200)

    contact_label = customtkinter.CTkLabel(app, font=font1, text='Contact:', text_color='#fff', bg_color='pink')
    contact_label.place(x=20, y=260)

    contact_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff',
                                           border_color='#0C9295', border_width=2, width=180)
    contact_entry.place(x=100, y=260)

    ClockInTime_label = customtkinter.CTkLabel(app, font=font1, text='ClockInTime:', text_color='#fff', bg_color='pink')
    ClockInTime_label.place(x=20, y=400)

    ClockInTime_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff',
                                           border_color='#0C9295', border_width=2, width=180)
    ClockInTime_entry.place(x=150, y=400)

    ClockOutTime_label = customtkinter.CTkLabel(app, font=font1, text='ClockOutTime:', text_color='#fff', bg_color='pink')
    ClockOutTime_label.place(x=370, y=400)

    ClockOutTime_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff',
                                           border_color='#0C9295', border_width=2, width=180)
    ClockOutTime_entry.place(x=520, y=400)

    add_button = customtkinter.CTkButton(app, command=insert, font=font1, text_color='#fff', text='Add Employee',
                                         fg_color='#05A321', hover_color='#00850B', bg_color='pink', cursor='hand2',
                                         corner_radius=15, width=260)
    add_button.place(x=20, y=310)

    clear_button = customtkinter.CTkButton(app, command=lambda: clear(True), font=font1, text_color='#fff',
                                           text='New Employee', fg_color='pink', hover_color='#FF5002',
                                           bg_color='pink', border_color='#F15704', border_width=2, cursor='hand2',
                                           corner_radius=15, width=260)
    clear_button.place(x=20, y=360)

    update_button = customtkinter.CTkButton(app, command=update, font=font1, text_color='#fff',
                                            text='Update Employee', fg_color='pink', hover_color='#FF5002',
                                            bg_color='pink', border_color='#F15704', border_width=2, cursor='hand2',
                                            corner_radius=15, width=260)
    update_button.place(x=300, y=360)

    delete_button = customtkinter.CTkButton(app, command=delete, font=font1, text_color='#fff',
                                            text='Delete Employee', fg_color='#E40404', hover_color='#AE0000',
                                            bg_color='pink', border_color='#E40404', border_width=2, cursor='hand2',
                                            corner_radius=15, width=260)
    delete_button.place(x=580, y=360)

    db_options = customtkinter.CTkComboBox(app, font=font1, text_color='#000', fg_color='#fff',
                                            dropdown_hover_color='#0C9295', button_color='#0C9295',
                                            button_hover_color='#0C9295', border_color='#0C9295', width=270,
                                            variable=selected_db_var, values=database_files, state='readonly')
    db_options.set('Choose Database File')
    db_options.place(x=28, y=550)

    update_table_button = customtkinter.CTkButton(app, command=choose_database_file, font=font1, text_color='#fff',
                                              text='Update Table', fg_color='#05A321', hover_color='#00850B',
                                              bg_color='pink', cursor='hand2', corner_radius=15, width=260)
    update_table_button.place(x=300, y=550)

    payroll_button = customtkinter.CTkButton(app, command=payroll_window, font=font1, text_color='#fff',
                                              text='Payroll System', fg_color='#05A321', hover_color='#00850B',
                                              bg_color='pink', cursor='hand2', corner_radius=15, width=260)
    payroll_button.place(x=300, y=470)

    style = ttk.Style(app)

    style.theme_use('clam')
    style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
    style.map('Treeview', background=[('selected', '#1A8F2D')])

    tree = ttk.Treeview(app, height=15)

    tree['columns'] = ('ID', 'Name', 'Role', 'Gender', 'Contact', 'ClockInTime', 'ClockOutTime')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', anchor=tk.CENTER, width=80)
    tree.column('Name', anchor=tk.CENTER, width=120)
    tree.column('Role', anchor=tk.CENTER, width=120)
    tree.column('Gender', anchor=tk.CENTER, width=100)
    tree.column('Contact', anchor=tk.CENTER, width=120)
    tree.column('ClockInTime', anchor=tk.CENTER, width=170)
    tree.column('ClockOutTime', anchor=tk.CENTER, width=170)

    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Role', text='Role')
    tree.heading('Gender', text='Gender')
    tree.heading('Contact', text='Contact')
    tree.heading('ClockInTime', text='ClockInTime')
    tree.heading('ClockOutTime', text='ClockOutTime')

    tree.place(x=300, y=20)

    tree.bind('<ButtonRelease>', display_data)

    add_to_treeview()

    app.mainloop()

login_window = Tk()
login_window.title('Admin Login')
login_window.geometry('1200x600')
login_window.resizable(False, False)

background_image = Image.open('background.jpg')
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(login_window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

sticker_size = (400, 180)
sticker_photo = resize_image('logo.jpg', sticker_size)
sticker_label = Label(login_window, image=sticker_photo)
sticker_label.place(x=400, y=100)

login_font = ('Arial', 14)

username_label = Label(login_window, text='Username:', font=login_font)
username_label.grid(row=0, column=0, padx=100, pady=(300, 10), sticky='e')  

username_entry = Entry(login_window, font=login_font)
username_entry.grid(row=0, column=1, padx=10, pady=(300, 10), sticky='w', columnspan=2)  

password_label = Label(login_window, text='Password:', font=login_font)
password_label.grid(row=1, column=0, padx=100, pady=(30, 10), sticky='e')  

password_entry = Entry(login_window, show='*', font=login_font)
password_entry.grid(row=1, column=1, padx=10, pady=(30, 10), sticky='w', columnspan=2)  

login_button = Button(login_window, text='Login', command=admin_login, font=login_font)
login_button.grid(row=2, column=0, columnspan=3, pady=(30, 10))

login_window.columnconfigure(0, weight=1)
login_window.columnconfigure(1, weight=1)
login_window.columnconfigure(2, weight=1)

login_window.mainloop()