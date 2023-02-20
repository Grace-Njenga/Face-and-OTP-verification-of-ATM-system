import tkinter as tk
from tkinter import messagebox
import random
import pymysql

#login verification process
def open_signin_window():
    def verify_otp(otp_received, entered_otp):
        if str(otp_received) == str(entered_otp):
            return True
        else:
            return False
        
    def verify_and_login():
        conn = pymysql.connect(host='localhost', user='NJENGA', passwd='mynewpass', database='atm', cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        account_number = account_number_entry.get()

        query = "SELECT phone_number FROM account_info WHERE account_number =%s"
        cursor.execute(query, (account_number,))
        result = cursor.fetchone()
        if result:
            #generate otp
            otp=random.randint(1000,9999)

            #store otp in the database
            query = "UPDATE account_info SET otp = %s WHERE account_number = %s"
            cursor.execute(query, (otp,account_number))

            #papa's main.py goes here 

            conn.commit()
        else:
            messagebox.showerror("Error","Invalid Account Number")
        #close cursor and database connection
        cursor.close()
        conn.close()

        # Open a new window to enter the OTP
        otp_window = tk.Toplevel()
        otp_window.geometry('460x250+150+100')
        otp_window.title("Verify OTP")
        otp_window.configure(bg='white')

        #entry widgets
        otp_label = tk.Label(otp_window, text="Enter OTP:",bg='white')
        otp_entry = tk.Entry(otp_window)

        def verify_otp_action (otp,stored_otp):
            if verify_otp(otp,stored_otp):
                messagebox.showinfo("info","OTP verified")

            else:
                messagebox.showerror("error","invalid OTP")

        #verify otp button
        verify_button = tk.Button(otp_window, text="VERIFY",bg='#57a1f8',width=39, pady=6, bd=0, height=2, cursor="hand2", command=lambda: verify_otp_action(otp, otp_entry.get())) #command=lambda: verify_otp_action(otp, otp_entry.get())
    
        otp_label.pack()
        otp_entry.pack()
        verify_button.pack(pady=20)
        signin_window.destroy()

    signin_window = tk.Toplevel()
    signin_window.geometry("925x500+300+200")
    signin_window.title("Sign In")
    signin_window.configure(bg="white")
    
    # Account Number field
    account_number_label = tk.Label(signin_window, text="Account Number:", bg="white", font=('Microsoft YaHei UI Light, bold', 11))
    account_number_label.pack()
    account_number_entry = tk.Entry(signin_window, width=25)
    account_number_entry.pack()

    login_button = tk.Button(signin_window, text="LOGIN", bg='#57a1f8' ,command=verify_and_login, width=39,pady=8, bd=0, height=2, cursor="hand2")
    login_button.pack(pady=20)

#REGISTER USER 
def register_form():
        # Connect to database
    connection = pymysql.connect(host='localhost',
                             user='NJENGA',
                             password='mynewpass',
                             db='atm',
                             cursorclass=pymysql.cursors.DictCursor)

    window = tk.Tk()
    window.title("SIGN UP")
    window.geometry("925x500+300+200")
    window.configure(bg='white')

    # Labels for form fields
    email_label = tk.Label(window, text="Email:", bg='white', font=('Microsoft YaHei UI Light, bold', 11))
    account_number_label = tk.Label(window, text="Account Number:", bg='white', font=('Microsoft YaHei UI Light, bold', 11))
    national_id_label = tk.Label(window, text="National ID:", bg='white', font=('Microsoft YaHei UI Light, bold', 11))
    phone_number_label = tk.Label(window, text="Phone Number:", bg='white', font=('Microsoft YaHei UI Light, bold', 11))

    # Entry fields for form
    email_entry = tk.Entry(window,width=25)
    account_number_entry = tk.Entry(window, width=25)
    national_id_entry = tk.Entry(window, width=25)
    phone_number_entry = tk.Entry(window, width=25)

    # Register button
    def register_button_click():
        email = email_entry.get()
        account_number = account_number_entry.get()
        national_id = national_id_entry.get()
        phone_number = phone_number_entry.get()

        # Insert user data into database
        with connection.cursor() as cursor:
            sql = "INSERT INTO account_info (email, account_number, national_ID, phone_number) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, account_number, national_id, phone_number))

        connection.commit()
        window.destroy()

    register_button = tk.Button(window, text="REGISTER", command=register_button_click, bg='#57a1f8', width=39, pady=7, bd=0, height=2, cursor="hand2")

    # Place form fields and buttons on window
    email_label.pack()
    email_entry.pack(pady=10)
    account_number_label.pack()
    account_number_entry.pack(pady=10)
    national_id_label.pack()
    national_id_entry.pack(pady=10)
    phone_number_label.pack()
    phone_number_entry.pack(pady=10)
    
    register_button.pack(pady=20)

    window.mainloop()

    # Main window
root = tk.Tk()
root.title("CHASE BANK ATM")
root.geometry("925x500+300+200")
root.configure( bg='white')

#label for the winodow
land_label= tk.Label(root, text='Welcome to Chase Bank', bg='white', \
    fg='black', font=("Helvetica", 16))
land_label.pack(pady=20)

# Signup and Login buttons
signup_button = tk.Button(root, text="SIGN UP", width=39, pady=7, bd=0, height=2, \
    cursor="hand2",command=register_form, bg='#57a1f8')
signin_button = tk.Button(root, text='SIGN IN', bg='#57a1f8',width=39, pady=7, bd=0, height=2, \
    cursor="hand2", command=open_signin_window)# command=login_form,

#display the buttons
signup_button.pack(pady=20)
signin_button.pack(pady=20)

root.mainloop()
