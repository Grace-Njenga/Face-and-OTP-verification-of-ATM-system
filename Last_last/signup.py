import pymysql
import tkinter as tk


# Registration form window
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

    # Send OTP button
    send_otp_button = tk.Button(window, text="SEND OTP", bg='#a857f8', width=39, pady=8, bd=0, height=2, \
    cursor="hand2")

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
    send_otp_button.pack(pady=20)
    register_button.pack(pady=20)

    window.mainloop()

# Main window
root = tk.Tk()
root.title("CHASE BANK ATM")
root.geometry("925x500+300+200")
root.configure(bg='white')

#label for the winodow
land_label= tk.Label(root, text='Welcome to Chase Bank', bg='white', \
    fg='black', font=("Helvetica", 16))
land_label.pack(pady=20)

# Signup and Login buttons
signup_button = tk.Button(root, text="SIGN UP", width=39, pady=7, bd=0, height=2, \
    cursor="hand2",command=register_form, bg='#57a1f8')
login_button = tk.Button(root, text='SIGN IN', bg='#57a1f8',width=39, pady=7, bd=0, height=2, \
    cursor="hand2")# command=login_form,

#display the buttons
signup_button.pack(pady=20)
login_button.pack(pady=20)

root.mainloop()
