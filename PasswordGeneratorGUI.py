import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
import sqlite3
import os
from tabulate import tabulate

def generate_password(length, include_special_chars, include_caps, include_nums):
    characters = string.ascii_lowercase
    if include_caps:
        characters += string.ascii_uppercase
    if include_nums:
        characters += string.digits
    if include_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for i in range(length))
    return password

def submit_options():
    password_length = password_length_scale.get()
    include_special_characters = special_characters_var.get()
    include_capital_letters = capital_letters_var.get()
    include_numbers = include_numbers_var.get()

    generated_password = generate_password(
        password_length,
        include_special_characters,
        include_capital_letters,
        include_numbers
    )

    password_display_var.set(generated_password)

def copy_to_clipboard():
    password = password_display_var.get()
    pyperclip.copy(password)
    messagebox.showinfo("Password Copied", "The password has been copied to the clipboard.")

def add_entry_to_db():
    entry_name = name_entry.get()
    entry_username = username_entry.get()
    entry_password = password_display_var.get()
    entry_user_id = user_id_entry.get()
    insert_password(entry_name, entry_username, entry_password, entry_user_id)

def insert_password(entry_name, entry_username, entry_password, entry_user_id):
    # Logic for inserting into the database
    # which also includes exception handling, etc.

    if not all([entry_name, entry_username, entry_password, entry_user_id]):  # Validate non-empty entries
        messagebox.showwarning("Incomplete Data", "Please fill in all fields.")
        return

def print_passwords_db():
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM passwords")
        rows = cursor.fetchall()
        cursor.execute("PRAGMA table_info(passwords)")
        column_names = [row[1] for row in cursor.fetchall()]
        print(tabulate(rows, headers=column_names, tablefmt='grid'))
    except Exception as e:
        print(f"An error occurred while reading from the database: {e}")
    finally:
        connection.close()

# Initialize the connection to the DB
database_file = "password_manager.db"

if not os.path.isfile(database_file):
    connection = sqlite3.connect(database_file)
    cursor =  connection.cursor()

    cursor.execute('''CREATE TABLE passwords (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,  -- This should be the encrypted password
                            user_id INTEGER NOT NULL
                          )''')
    cursor.execute("INSERT INTO passwords (id, name, username, password, user_id) VALUES (?, ?, ?, ?, ?)", ('000001','Jacen Martin', 'Jacen_Martin', 'example_password', 'Jacen_Martin'))
    connection.commit()
    cursor.execute("SELECT * FROM passwords")
    rows = cursor.fetchall()
    cursor.execute("PRAGMA table_info(passwords)")
    column_names = [row[1] for row in cursor.fetchall()]
    print(tabulate(rows, headers=column_names, tablefmt='grid'))
    connection.close()


# Create the main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x400")  # Set the window size

# Define a font for the widgets
label_font = ('Arial', 10)
entry_font = ('Arial', 12, 'bold')
button_font = ('Arial', 10, 'bold')

tk.Label(root, text="Enter the name:", font=label_font).grid(row=7, column=0, sticky='w', padx=5, pady=5)
name_entry = tk.Entry(root, font=entry_font)
name_entry.grid(row=7, column=1, padx=5, pady=5)

# Label and Entry for Username
tk.Label(root, text="Enter the username:", font=label_font).grid(row=8, column=0, sticky='w', padx=5, pady=5)
username_entry = tk.Entry(root, font=entry_font)
username_entry.grid(row=8, column=1, padx=5, pady=5)

# Label and Entry for User ID
tk.Label(root, text="Enter the user ID:", font=label_font).grid(row=9, column=0, sticky='w', padx=5, pady=5)
user_id_entry = tk.Entry(root, font=entry_font)
user_id_entry.grid(row=9, column=1, padx=5, pady=5)

# Submit Button to Add Entry to DB
submit_button = tk.Button(root, text="Add Entry to DB", command=add_entry_to_db, font=button_font)
submit_button.grid(row=10, columnspan=2, padx=5, pady=5)

special_characters_var = tk.BooleanVar()
capital_letters_var = tk.BooleanVar()
include_numbers_var = tk.BooleanVar()
password_display_var = tk.StringVar(root)

# Password Length Scale
tk.Label(root, text="Select the length of the password (1-64):", font=label_font).grid(row=0, column=0, sticky='e', padx=5, pady=5)
password_length_scale = tk.Scale(root, from_=1, to=64, orient='horizontal', length=200, font=label_font)
password_length_scale.set(14)
password_length_scale.grid(row=0, column=1, pady=5)

# Special Characters Checkbox
tk.Checkbutton(root, text="Include special characters", variable=special_characters_var, font=label_font).grid(row=1, columnspan=2, sticky='w', padx=5, pady=2)

# Capital Letters Checkbox
tk.Checkbutton(root, text="Include capital letters", variable=capital_letters_var, font=label_font).grid(row=2, columnspan=2, sticky='w', padx=5, pady=2)

# Numbers Checkbox
tk.Checkbutton(root, text="Include numbers", variable=include_numbers_var, font=label_font).grid(row=3, columnspan=2, sticky='w', padx=5, pady=2)

# Generate Password Button
generate_button = tk.Button(root, text="Generate Password", command=submit_options, font=button_font)
generate_button.grid(row=4, columnspan=2, padx=5, pady=5)

# Password Display Entry
password_display_entry = tk.Entry(root, textvariable=password_display_var, state="readonly", width=50, font=entry_font)
password_display_entry.grid(row=5, columnspan=2, padx=5, pady=5)

# Copy to Clipboard Button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=button_font)
copy_button.grid(row=6, columnspan=2, padx=5, pady=5)

def insert_password(entry_name: object, entry_username: object, entry_password: object, entry_userid: object) -> None:
    if not all([entry_name, entry_username, entry_password, entry_userid]):  # Validate inputs are not empty
        messagebox.showwarning("Incomplete Data", "Please fill in all fields.")
    else:
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO passwords (name, username, password, user_id) VALUES (?, ?, ?, ?)",
                      (entry_name, entry_username, entry_password, entry_userid))

        connection.commit()
        connection.close()
        messagebox.showinfo("Entry Added", "The password entry has been added to the database.")

def add_entry_to_db():
    entry_name = name_entry.get()
    entry_username = username_entry.get()
    entry_password = password_display_var.get()
    entry_userid = user_id_entry.get()

    insert_password(entry_name, entry_username, entry_password, entry_userid)

# Add entry widgets and a submit button to the main window
name_entry = tk.Entry(root, font=entry_font)
name_entry.grid(row=7, column=1, padx=5, pady=5)

username_entry = tk.Entry(root, font=entry_font)
username_entry.grid(row=8, column=1, padx=5, pady=5)

user_id_entry = tk.Entry(root, font=entry_font)
user_id_entry.grid(row=9, column=1, padx=5, pady=5)

submit_button = tk.Button(root, text="Add Entry to DB", command=add_entry_to_db, font=button_font)
submit_button.grid(row=10, columnspan=2, padx=5, pady=5)

root.mainloop()

print_passwords_db()