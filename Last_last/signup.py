import tkinter as tk
from tkinter import messagebox
import random
import pymysql

# Function to open the sign in window
def open_signin_window():

    signin_window = tk.Toplevel()
    signin_window.geometry("925x500+300+200")
    signin_window.title("Sign In")
    signin_window.configure(bg="white")
    
    # Account Number field
    account_number_label = tk.Label(signin_window, text="Account Number:", bg="white", font=('Microsoft YaHei UI Light, bold', 11))
    account_number_label.pack()
    account_number_entry = tk.Entry(signin_window, width=25)
    account_number_entry.pack()

##########################ACCOUNT NUMBER AND OTP GENERATION AND VERIFICATION STARTS########################## 
##############################################################################################################
    def verify_otp(otp_received, entered_otp):
        if str(otp_received) == str(entered_otp):
            return True
        else:
            return False
      
    # Login button
    def verify_and_login():
        # Connect to the database
        conn = pymysql.connect(host="localhost", user="NJENGA", password="mynewpass", database="atm")
        cursor = conn.cursor()

        account_number = account_number_entry.get()
        
        # Verify if the account number exists in the database
        query = "SELECT phone_number FROM account_info WHERE account_number = %s"
        cursor.execute(query, (account_number,))
       
        result = cursor.fetchone()

        # Code to verify in database goes here
        if result:
            #phone_number=result[0]

            #generate OTP
            otp=random.randint(1000,9999)

            #store otp in the database
            sql='UPDATE account_info SET otp=%s WHERE account_number =%s'
            cursor.execute(sql,(otp,account_number))

            #sms API GOES HERE
            
            conn.commit()
            # Account number exists, take appropriate action that is show OTP window
            #1st show that account was found successfully then open another window
            print("Account number exists in the database")
            #messagebox.showinfo("Info", "Account Verified!")
        else:
            # Account number does not exist, take appropriate action
            print("Account number does not exist in the database")
            messagebox.showerror("Error", "INVALID ACCOUNT NUMBER")

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Open a new window to enter the OTP
        otp_window = tk.Toplevel()
        otp_window.geometry('460x250+150+100')
        otp_window.title("Verify OTP")
        otp_window.configure(bg='white')
    
        otp_label = tk.Label(otp_window, text="Enter OTP:",bg='white')
        otp_entry = tk.Entry(otp_window)
        verify_button = tk.Button(otp_window, text="VERIFY",bg='#57a1f8',width=39, pady=6, bd=0, height=2, cursor="hand2", command=lambda: verify_otp_action(otp, otp_entry.get())) #command=lambda: verify_otp_action(otp, otp_entry.get())
    
        otp_label.pack()
        otp_entry.pack()
        verify_button.pack(pady=20)
        signin_window.destroy()

        #verification of otp
        def verify_otp_action(otp,stored_otp):
            if verify_otp(otp,stored_otp):
                messagebox.showinfo("Info", "OTP IS VALID")
                print('OTP sent successfully')
                switch_window()
            else:
                messagebox.showerror("Error", "INVALID OTP")
                print('OTP not received')
############################################################################################################
##########################ACCOUNT NUMBER AND OTP GENERATION AND VERIFICATION ENDS###########################

    login_button = tk.Button(signin_window, text="LOGIN", bg='#57a1f8' ,command=verify_and_login, width=39,pady=8, bd=0, height=2, cursor="hand2")
    login_button.pack(pady=20)

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

#after OTP enter
#withdraw or deposit window

def toa():
        # Connect to the database
    #connection = pymysql.connect(host="localhost", user="NJENGA", password="mynewpass", database="atm")

    toa_win = tk.Toplevel()
    #toa_win.title = ('WITHDRAW')
    toa_win.geometry('460x250+150+100')

    amnt_label = tk.Label(toa_win, text="Enter Amount:",bg='white')
    amnt_entry = tk.Entry(toa_win)
    amnt_label.pack()
    amnt_entry.pack()

def switch_window():
    root.withdraw()

    new_window = tk.Tk()
    new_window.title("C H A S E  B A N K")
    new_window.geometry("925x500+300+200")
    new_window.configure( bg='white')
    # Add widgets to new window

    #label for the winodow
    title= tk.Label(new_window, text='Choose from either:', bg='white', \
        fg='black', font=("Helvetica", 16))
    title.pack(pady=20)
        
    withdraw_button = tk.Button(new_window, text="WITHDRAW", width=39, pady=7, bd=0, height=2, \
        cursor="hand2", bg='#57a1f8',command=toa)#command=toa
    deposit_button = tk.Button(new_window, text='DEPOSIT', bg='#57a1f8',width=39, pady=7, bd=0, height=2,
        cursor="hand2") #command=weka

    #display the buttons
    withdraw_button.pack(pady=20)
    deposit_button.pack(pady=20)

    new_window.mainloop()

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

