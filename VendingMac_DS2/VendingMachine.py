import customtkinter
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageSequence

purchase_history = []

def insert_sticker(app):
    sticker_image = Image.open('A1.jpg')
    sticker_image = sticker_image.resize((410, 598))
    sticker_photo = ImageTk.PhotoImage(sticker_image)

    sticker_label = tk.Label(app, image=sticker_photo, bg='white')
    sticker_label.image = sticker_photo
    sticker_label.place(x=878, y=98)

def animate_bg(idx=0):
    background_label.config(image=background_frames[idx])
    idx = (idx + 1) % len(background_frames)
    app.after(100, animate_bg, idx)

def update_balance(amount):
    current_balance = float(balance.get())
    new_balance = current_balance + amount
    balance.delete(0, tk.END)
    balance.insert(0, str(new_balance))

def update_total(item_price):
    current_total = float(total.get())
    new_total = current_total + item_price
    total.delete(0, tk.END)
    total.insert(0, str(new_total))


def compute_remaining_balance(purchase_history_label, item_price):
    current_balance = float(balance.get())
    current_total = float(total.get())
    remaining_balance = current_balance - current_total
    balance.delete(0, tk.END)
    balance.insert(0, str(remaining_balance))
    total.delete(0, tk.END)
    total.insert(0, "0")
    
    purchase_history_label.place_forget()



def add_to_purchase_history(item, price, purchase_history_label):
    purchase_history.append((item, price))
    purchase_history_label.configure(text="\n".join(f"{item}: ₱{price}" for item, price in purchase_history))


def main_window():
    global app, background_label, background_frames, balance, total, purchase_history_label

    app = customtkinter.CTk()
    app.title('Beverage Vending Machine')
    app.geometry('1800x900')
    app.config(bg='lightblue')
    app.resizable(False, False)

    background_label = tk.Label(app)
    background_label.place(x=0, y=0)

    background_frames = []
    background_gif = Image.open('mew.gif')
    for frame in ImageSequence.Iterator(background_gif):
        frame = frame.resize((1800, 900))
        background_frames.append(ImageTk.PhotoImage(frame))

    animate_bg()

    canvas = tk.Canvas(app, width=600, height=800)
    canvas.place(x=840, y=50)

    canvas.create_rectangle(3, 800, 600, 3, outline='black', width=2, fill='grey')
    canvas.create_rectangle(40, 650, 450, 50, outline='lightgrey', width=2, fill='white')

    money_slot = customtkinter.CTkLabel(app, font=('Arial', 10), text='___________________', text_color='grey', bg_color='black')
    money_slot.place(x=1300, y=480)

    balance_label = customtkinter.CTkLabel(app, font=('Arial', 15), text='↑ Insert a bill\n or a coin →', text_color='white', bg_color='black')
    balance_label.place(x=1300, y=520)

    coin_slot = customtkinter.CTkLabel(app, font=('Arial', 15), text='  l  ', text_color='grey', bg_color='black')
    coin_slot.place(x=1390, y=530)

    balance = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='black', fg_color='white', border_color='black',
                                       border_width=2, width=130)
    balance.insert(tk.END, "0")  
    balance.place(x=1300, y=570)

    money_text = customtkinter.CTkLabel(app, font=('Arial', 20), text='  How much money do you have?  ', text_color='white', bg_color='black')
    money_text.place(x=200, y=470)

    total_label = customtkinter.CTkLabel(app, font=('Arial', 15), text='Select drinks and\n know its total price', text_color='white', bg_color='black')
    total_label.place(x=1300, y=620)

    purchase_history_label = customtkinter.CTkLabel(app, font=('Arial', 15), text='Purchase History:', text_color='white', bg_color='black')
    purchase_history_label.place(x=50, y=650)
    purchase_history_label.place_forget()


    total = customtkinter.CTkEntry(app, font=('Arial', 16), text_color='black', fg_color='white', border_color='black',
                                       border_width=2, width=130)
    total.insert(tk.END, "0")
    total.place(x=1300, y=660)

    A1_price = 30
    A1 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='A1',
                             fg_color='black', hover_color='darkblue', bg_color='grey',
                             cursor='hand2', corner_radius=15, width=120,
                             command=lambda: (update_balance(0), update_total(A1_price), add_to_purchase_history("A1", A1_price, purchase_history_label)))

    A1.place(x=1300, y=110)

    A2_price = 30
    A2 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='A2',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(A2_price), add_to_purchase_history("A2", A2_price, purchase_history_label)))
    A2.place(x=1300, y=150)

    A3_price = 25
    A3 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='A3',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(A3_price), add_to_purchase_history("A3", A3_price, purchase_history_label)))
    A3.place(x=1300, y=190)

    B1_price = 30
    B1 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='B1',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(B1_price), add_to_purchase_history("B1", B1_price, purchase_history_label)))
    B1.place(x=1300, y=230)

    B2_price = 50
    B2 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='B2',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(B2_price), add_to_purchase_history("B2", B2_price, purchase_history_label)))
    B2.place(x=1300, y=270)

    B3_price = 55
    B3 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='B3',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(B3_price), add_to_purchase_history("B3", B3_price, purchase_history_label)))
    B3.place(x=1300, y=310)

    C1_price = 60
    C1 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='C1',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(C1_price), add_to_purchase_history("C1", C1_price, purchase_history_label)))
    C1.place(x=1300, y=350)

    C2_price = 10
    C2 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='C2',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(C2_price), add_to_purchase_history("C2", C2_price, purchase_history_label)))
    C2.place(x=1300, y=390)

    C3_price = 15
    C3 = customtkinter.CTkButton(app, font=('Arial', 16), text_color='#fff', text='C3',
                            fg_color='black', hover_color='darkblue', bg_color='grey',
                            cursor='hand2', corner_radius=15, width=120,
                            command=lambda: (update_balance(0), update_total(C3_price), add_to_purchase_history("C3", C3_price, purchase_history_label)))
    C3.place(x=1300, y=430)

    Claim_here = customtkinter.CTkButton(app, font=('Arial', 20), text_color='#fff', text='Claim here ',
                                     fg_color='black', hover_color='darkblue', bg_color='grey',
                                     cursor='hand2', corner_radius=10, width=190, height=80,
                                     command=lambda: (compute_remaining_balance(purchase_history_label, A1_price), show_purchase_history(purchase_history_label)))


    Claim_here.place(x=910, y=730)

    payb_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱5 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(5))
    payb_pesos.place(x=200, y=505)

    ten_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱10 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(10))
    ten_pesos.place(x=350, y=505)

    bente_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱20 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(20))
    bente_pesos.place(x=500, y=505)

    fipty_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱50 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(50))
    fipty_pesos.place(x=650, y=505)

    isalibo_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱100 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(100))
    isalibo_pesos.place(x=200, y=550)

    duhalibo_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱200 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(200))
    duhalibo_pesos.place(x=350, y=550)

    limalibo_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱500 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(500))
    limalibo_pesos.place(x=500, y=550)

    thousand_pesos = customtkinter.CTkButton(app, font=('Arial', 20), text_color='white', text='₱1000 ',
                                            fg_color='green', hover_color='darkblue', bg_color='black',
                                            cursor='hand2', corner_radius=10, width=120, command=lambda: update_balance(1000))
    thousand_pesos.place(x=650, y=550)

    title_text = "BevMac"
    canvas.create_text(450, 750, text=title_text, font=("Impact", 50), fill="black")

    insert_sticker(app) 

    app.mainloop()

def show_purchase_history(purchase_history_label):
    purchase_history_label.place(x=520, y=650)

main_window()
