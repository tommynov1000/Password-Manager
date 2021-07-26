from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
from pyperclip import copy
import json

EMAIL = "tommynov@vt.edu"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    global data
    website = website_entry.get().strip()
    password = password_entry.get().strip()
    username = username_entry.get().strip()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if website == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("..//passwords.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            data = new_data
        else:
            # Updating old data with new data
            data.update(new_data)
        finally:
            with open("..//passwords.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
            password_entry.delete(0, END)
            website_entry.delete(0, END)


# ---------------------------- PASSWORD SEARCH ------------------------------- #
def find_password():
    website = website_entry.get().strip()

    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("..//passwords.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No Data File Found.")
        else:
            if website in data:
                username = data[website]["username"]
                password = data[website]["password"]
                copy(password)
                messagebox.showinfo(title="Credentials Found", message=f"Username: {username}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Oops", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #

# Window setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Password Setup
canvas = Canvas(width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=1)

# website entry setup
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry()
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="EW")

# Website search setup
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

# username entry setup
username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)
username_entry = Entry()
username_entry.insert(0, EMAIL)
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

# password entry and button setup
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry()
password_entry.grid(row=3, column=1, sticky="EW")
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2, sticky="EW")

# add button setup
add_button = Button(text="Add", command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

# window mainloop
window.mainloop()
