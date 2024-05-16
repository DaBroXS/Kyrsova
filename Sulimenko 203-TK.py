import tkinter as tk
from tkinter import messagebox
import re
import pandas as pd
import math 

data = pd.read_csv("contacts.csv")


number_pattern = re.compile(r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")

def print_contacts():
    contact_list.delete(0, tk.END)
    data_to_print = data 
    search = search_entry.get()
    if len(search) > 0:
        data_to_print =data[(data["name"].str.contains(search)) | (data["number"].str.contains(search)) | (data["home_number"].str.contains(search))]
    for index, row in data_to_print.sort_values(by= "name").iterrows():
        contact_list.insert(index,str(index) + ") " + str(row['name']) + ": " + str(row['number']) +";"+"  email: " + str(row['email']))

def save_contacts():
    data.to_csv("contacts.csv", index=False)

def add_contact():
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    home_number = home_number_entry.get()

    if not number_pattern.fullmatch(number):
            messagebox.showerror("Wrong phone", "Entered phone number was not in correct format")
            return
    if name and number:
       
        data.loc[len(data)] = {
            "name": name_entry.get(),
            "address": address_entry.get(),
            "email": email_entry.get(),
            "number": number_entry.get(),
            "home_number": home_number_entry.get()
        }
        print_contacts()
        save_contacts()

        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        home_number_entry.delete(0, tk.END)
        
    else:
        messagebox.showerror("Error", "Please enter both name and number.")

def delete_contact():
    try:
        selected_index = contact_list.curselection()[0]
        contact_list.delete(selected_index)
        data.drop(selected_index, inplace=True)
        save_contacts()

    except IndexError:
        messagebox.showerror("Error", "No contact selected.")

def edit_contact():
    try:
        selected_index = contact_list.curselection()[0]
        selected_index = int(contact_list.get(contact_list.curselection()).split(")")[0])
        name = name_entry.get()
        number = number_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        home_number = home_number_entry.get()

        if not number_pattern.fullmatch(number):
            messagebox.showerror("Wrong phone", "Entered phone number was not in correct format")
            return
        if name and number:
       
            data.loc[selected_index] = {
                "name": name_entry.get(),
                "address": address_entry.get(),
                "email": email_entry.get(),
                "number": number_entry.get(),
                "home_number": home_number_entry.get()
            }
            print_contacts()
            save_contacts()

            name_entry.delete(0, tk.END)
            number_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            home_number_entry.delete(0, tk.END)
        
        else:
            messagebox.showerror("Error", "Please enter both name and number.")

    except IndexError:
        messagebox.showerror("Error", "No contact selected.")
    


def on_contact_click(event):
    try:
        selected_index = contact_list.curselection()[0]
        selected_index = int(contact_list.get(contact_list.curselection()).split(")")[0])
        contact = data.loc[selected_index]
        name = contact['name']
        number = contact['number']
        email = contact['email']
        address = contact['address']
        home_number = contact['home_number']

        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        home_number_entry.delete(0, tk.END)

        if not is_empty_or_nan(name): name_entry.insert(0, name)
        if not is_empty_or_nan(number):number_entry.insert(0, number)
        if not is_empty_or_nan(address):address_entry.insert(0, address)
        if not is_empty_or_nan(email):email_entry.insert(0, email)
        if not is_empty_or_nan(home_number):home_number_entry.insert(0, home_number)

    except IndexError:
        messagebox.showerror("Error", "No contact selected.")

def is_empty_or_nan(var):
    if var is None:
        return True
    elif isinstance(var, float) and math.isnan(var):
        return True
    elif isinstance(var, str) and len(var.strip()) == 0:
        return True
    else:
        return False

def open_window():
    window = tk.Toplevel()
    window.geometry("600x550")

    window.title("Instruction")
    label1 = tk.Label(window, text= "Instructions for the phone book",font="Helvetica 16 bold", wraplength=600)
    label1.pack(fill=tk.X, expand=True)
    label2 = tk.Label(window, wraplength=600, text= "The phone directory is a tool for managing contacts' information. It stores data such as full name, address, email, and phone numbers (mobile and home) in a CSV file.", font="Helvetica 12")
    label2.pack(fill=tk.X, expand=True)
    label3 = tk.Label(window, wraplength=600, text= "Functionality:\n1.Add New Contacts: You can add new contacts to the directory by providing their information including full name, address, email, and one or more phone numbers. \n 2.Edit Existing Contacts: Existing contacts can be edited to update their information. You can add, remove, or modify phone numbers associated with a contact.\n 3.View Existing Contacts: You can view all contacts in the directory. The contacts will be displayed in sorted order, making it easy to find specific entries. \n 4.Delete Contacts: Contacts can be deleted from the directory if they are no longer needed. \n 5.Search by Parameters: You can search for contacts by specifying parameters such as last name or phone number.", font="Helvetica 13")
    label3.pack(fill=tk.X, expand=True)
    Label5 = tk.Label(window, font="Helvetica 12",text="1.Run the program\n2.Choose an option from the menu \n3.Follow the on-screen instructions for each option to complete the desired action.\nThese instructions help you manage contacts effectively using the phone directory tool.")
    Label5.pack(fill=tk.X, expand=True)




root = tk.Tk()
root.title("Phonebook")
root.geometry("600x550")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(9, weight=1)

header_frame = tk.Frame(root, background='lightgrey', )
header_frame.grid(row = 0, padx=5, pady=5, sticky=tk.W + tk.E, columnspan=2)

header = tk.Label(header_frame, text="Phonebook", font="Helvetica 16 bold", height=2 , background="lightgrey")
header.pack( padx=5, pady=5, side= tk.LEFT)

button_search = tk.Button(header_frame, text = "🔍", command=print_contacts)
button_search.pack( padx=5, pady=5, side= tk.RIGHT)

search_entry = tk.Entry(header_frame, width=30)
search_entry.pack( padx=5, pady=5, side= tk.RIGHT)


name_label = tk.Label(root, text="Name:")
name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

number_label = tk.Label(root, text="Number:")
number_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
number_entry = tk.Entry(root)
number_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

addres_label = tk.Label(root, text="Address:")
addres_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
address_entry = tk.Entry(root)
address_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

email_label = tk.Label(root, text="Email:")
email_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
email_entry = tk.Entry(root)
email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

home_number_label = tk.Label(root, text="Home number:")
home_number_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
home_number_entry = tk.Entry(root)
home_number_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

add_button = tk.Button(root, text="Add Contact", command=add_contact)
add_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

edit_button = tk.Button(root, text="Edit Contact", command=edit_contact)
edit_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

delete_button = tk.Button(root, text="Delete Contact", command=delete_contact)
delete_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

contact_list_frame = tk.Frame(root)
contact_list_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

scrollbar = tk.Scrollbar(contact_list_frame)
scrollbar.pack(side = tk.RIGHT, fill=tk.Y )

contact_list = tk.Listbox(contact_list_frame, font='Helvetica 14', yscrollcommand = scrollbar.set)
contact_list.pack(fill = tk.BOTH, expand=True)
contact_list.bind("<ButtonRelease-1>", on_contact_click)

scrollbar.config( command =  contact_list.yview )

print_contacts()

button_second_window = tk.Button(header_frame, text ='Instruction', command=open_window)
button_second_window.pack(padx=5, pady=5, side= tk.RIGHT)


root.mainloop()

