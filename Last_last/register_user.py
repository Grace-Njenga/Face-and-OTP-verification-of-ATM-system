import tkinter as tk
import pymysql
import random

def register_user():
    # Connect to the database
    conn = pymysql.connect(
        host='localhost',
        user='NJENGA',
        password='mynewpass',
        db='tryout'
    )
    cursor = conn.cursor()
    
    # Generate a random 4-digit OTP
    #otp = str(random.randint(1000, 9999))
    
    # Insert the new user into the "try" table
    sql = "INSERT INTO try (account_number, email, phone_number, national_id, otp) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (account_number.get(), email.get(), phone_number.get(), national_id.get(), otp))
    conn.commit()
    conn.close()
    
    # Show the OTP verification window
    verify_otp_window = tk.Tk()
    verify_otp_window.title("Verify OTP")
    verify_otp_window.geometry('925x500+300+200')
    
    # Add the OTP entry field and verification button to the window
    tk.Label(verify_otp_window, text="Enter OTP:").pack()
    otp_entry = tk.Entry(verify_otp_window)
    otp_entry.pack()
    tk.Button(verify_otp_window, text="Verify", command=lambda: verify_otp(otp, otp_entry.get(), verify_otp_window)).pack()

def verify_otp(sent_otp, entered_otp, window):
    if sent_otp == entered_otp:
        # Show the login success message
        tk.Label(window, text="Login Successful").pack()
    else:
        # Show the login failed message
        tk.Label(window, text="Login Failed").pack()

# Create the main window
root = tk.Tk()
root.title("Register")
root.geometry('925x500+300+200')

# Add the registration form to the main window
tk.Label(root, text="Account Number:").pack()
account_number = tk.Entry(root)
account_number.pack()
tk.Label(root, text="Email:").pack()
email = tk.Entry(root)
email.pack()
tk.Label(root, text="Phone Number:").pack()
phone_number = tk.Entry(root)
phone_number.pack()
tk.Label(root, text="National ID:").pack()
national_id = tk.Entry(root)
national_id.pack()
tk.Button(root, text="Register", command=register_user).pack()

root.mainloop()
