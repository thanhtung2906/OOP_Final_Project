import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
import os

# File paths
user_file_path = r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\login\user_login_data.csv"
admin_file_path = r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\login\admin_login_data.csv"

# Load data from CSV if exists, else create empty DataFrame
if os.path.exists(user_file_path):
    user_df = pd.read_csv( r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\login\user_login_data.csv",encoding='utf-8')

else:
    user_df = pd.DataFrame(columns=["Username"])

if os.path.exists(admin_file_path):
    admin_df = pd.read_csv(r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\login\admin_login_data.csv", encoding='utf-8')  # Hoặc thử 'latin1'

else:
    admin_df = pd.DataFrame(columns=["Username", "Password"])

# Function for User Login
def login_as_user():
    # Prompt to enter username
    user_name = simpledialog.askstring("User Login", "Please enter your username:")
    
    if user_name:
        # Add user to the user DataFrame and save to CSV
        new_user = pd.DataFrame([[user_name]], columns=["Username"])
        global user_df
        user_df = pd.concat([user_df, new_user], ignore_index=True)
        user_df.to_csv(user_file_path, index=False)
        
        messagebox.showinfo("Welcome", f"Welcome, {user_name}!")
    else:
        messagebox.showwarning("Input Error", "Username cannot be empty!")

# Function for Admin Login
def login_as_admin():
    # Create a new window for Admin Login
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Login")
    
    tk.Label(admin_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(admin_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(admin_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(admin_window, show="*")  # Hide password input
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Function to verify admin credentials
    def admin_login():
        username = username_entry.get()
        password = password_entry.get()

        # Check if username and password match with admin DataFrame
        admin_match = admin_df[(admin_df['Username'] == username) & (admin_df['Password'] == password)]
        
        if username and password:
            if not admin_match.empty:  # If match is found
                messagebox.showinfo("Login Successful", f"Welcome Admin, {username}!")
                admin_window.destroy()  # Close the login window after successful login
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password.")
        else:
            messagebox.showwarning("Input Error", "Both fields are required!")

    login_button = tk.Button(admin_window, text="Login", command=admin_login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Main Window Setup
root = tk.Tk()
root.title("Online Newspaper Reader")
root.geometry("500x400")

# Buttons for User and Admin Login
user_button = tk.Button(root, text="Login as User", width=20, command=login_as_user)
user_button.pack(pady=20)

admin_button = tk.Button(root, text="Login as Admin", width=20, command=login_as_admin)
admin_button.pack(pady=20)

root.mainloop()
