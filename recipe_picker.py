"""Recipe Picker"""
import tkinter as tk
import sqlite3
from PIL import ImageTk
import tkmacosx
from numpy import random

# variables
BG_COLOR = "#3d6466"

# functions
def clear_widgets(frame):
    """clear_widgets() function will clear the widgets in the frame"""
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    """fetch_db() function will fetch the database and return the data"""
    ### databse structure
    # Each seperate table is a recipe
    # Table name is the recipe name
    # Row/Records are ingredients
    # Columns/fields are id index 0, name index 1, and quantity index 2, and unit index 3

    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()
    #fetch random table
    idx = random.randint(0, len(all_tables)-1)
    #fetch ingredients from table
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name)
    table_records = cursor.fetchall()


    connection.close()
    return table_name, table_records

def pre_process(table_name, table_records):
    """pre_process() function will pre-process the data"""
    #title
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    #ingredients
    ingredients = []
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)
    
    return title, ingredients

def load_frame1():
    """load_frame1() function will load the first frame"""
    clear_widgets(frame2)
    frame1.tkraise() #tkraise() method raises the frame to the top of the stack
    frame1.pack_propagate(False)
    # frame1 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(
        frame1,
        text="ready for your random recipe?",
        bg=BG_COLOR,
        fg="white",
        font=("TkMenuFont", 14),
    ).pack()

    # button widget
    tkmacosx.Button(
        frame1,
        text="Pick a Recipe",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        # anonymous function that calls the load_frame
        command=lambda: load_frame2(),
    # padding goes in the .pack() method because the method renders the widget
    ).pack(pady=20)

def load_frame2():
    """Load frame2 when button is clicked"""
    clear_widgets(frame1)
    frame2.tkraise()

    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    # frame2 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    tk.Label(
        frame2,
        text=title,
        bg=BG_COLOR,
        fg="white",
        font=("TkHeadingFont", 20),
    ).pack(pady=25)

    for i in ingredients:
        tk.Label(
            frame2,
            text=i,
            bg="#28393a",
            fg="white",
            font=("TkMenuFont", 12),
            ).pack(fill="both", expand=True)
        
    tkmacosx.Button(
        frame2,
        text="BACK",
        font=("TkHeadingFont", 18),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        # anonymous function that calls the load_frame
        command=lambda: load_frame1(),
        ).pack(pady=20)

# initiallize app/window opject we are calling loop
root = tk.Tk()
root.title("Recipe Picker")
# eval method is used to execute a command in the tcl interpreter
root.eval("tk::PlaceWindow . center")

# create a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=BG_COLOR)
frame2 = tk.Frame(root, bg=BG_COLOR)
frame1.grid(row=0, column=0)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nsew")

load_frame1()

# call mainloop method that displays our window untill we hit the Exit button
root.mainloop()