#from tkinter import *
import tkinter as tk
import pymysql
#import random


def on_login_click():
  # Connect to the database
    conn = pymysql.connect(
        host='localhost',
        user='NJENGA',
        password = 'mynewpass',
        db='tryout'
    )
    cursor = conn.cursor()

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry('925x500+300+200')
    login_window.configure(bg='#fff')
    login_window.resizable(False,False)

    title_label=tk.Label(login_window, text='LOG IN', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    title_label.place(x=100, y=5)

    # Entry fields for account number and phone number/ email
    account= tk.Entry(login_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    account.place(x=30, y=80)
    account.insert(0, 'Enter Account Number')
    account.bind('<FocusIn>', lambda e: account.delete(0, 'end'))
    account.bind('<FocusOut>', lambda e: account.insert(0, 'Enter Account Number') if account.get() == "" else None)

    black=tk.Frame(login_window, width=295, height=2, bg='black')
    black.place(x=25,y=107)

    #EMAIL ENTRY FIELD
    email = tk.Entry(login_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    email.place(x=30, y=150)
    email.insert(0, 'Enter your Email')
    email.bind('<FocusIn>', lambda e: email.delete(0, 'end'))
    email.bind('<FocusOut>', lambda e: email.insert(0, 'Enter your Email') if email.get() == "" else None)

    black2=tk.Frame(login_window, width=295, height=2, bg='black')
    black2.place(x=25,y=177)

    #OTP verification button
    otp_button = tk.Button(login_window, width=39, pady=7, text="Send OTP", \
        bg='#57a1f8' ,fg='white', cursor="hand2" ,border=0, \
            command=lambda: on_otp_click(account.get(), email.get()))#command=lambda: on_otp_click(account.get(), email.get()).grid(row=2, column=1, sticky="E") on_otp_click(account, email)
    otp_button.place(x=35, y=204)

    #dont have an account yet
    label=tk.Label(login_window,text="Don't have an account?" , \
    fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=75,y=270)

    register_btn=tk.Button(login_window, text='Sign Up', width=6, fg='#57a1f8', border=0, bg='white', cursor='hand2',command=on_signup_click)
    register_btn.place(x=215, y=270)

    def on_otp_click(account, email):#
    # Prepare the SQL query
        query = "SELECT * FROM account_info WHERE email=%s AND account=%s"
        cursor.execute(query, (email, account))

        # Fetch the results
        cursor.execute("SELECT * FROM account_info WHERE account='" + account + "' AND email='" + email + "'")
        result = cursor.fetchone()

        if result:
            #Log in successful, do something here or take user to the otp verification window
            print("Login successful")
        else:
            # Log in unsuccessful, do something here include a message box
            print("Email not registered")


        #close connection and cursor
        conn.close()
        cursor.close

    login_window.mainloop()

def on_signup_click():
    # Connect to the database
    conn = pymysql.connect(
        host='localhost',
        user='NJENGA',
        password = 'mynewpass',
        db='tryout'
    )
    cursor = conn.cursor()
    
    # Generate a random 4-digit OTP
    #otp = str(random.randint(1000, 9999))
    
    register_window = tk.Tk()
    register_window.title("Register")
    register_window.geometry('925x500+300+200')
    register_window.configure(bg='#fff')
    register_window.resizable(False,False)

    title_label=tk.Label(register_window, text='REGISTER HERE!', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    title_label.place(x=100, y=5)

    # Entry fields for account_number, national_ID, phone_number, and email

    #Account number entry
    account_number= tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    account_number.place(x=30, y=80)
    account_number.insert(0, 'Enter Account Number')
    #account_number.bind('<FocusIn>', lambda e: account_number.delete(0, 'end'))
    #account_number.bind('<FocusOut>', lambda e: account_number.insert(0, 'Enter Account Number') if account_number.get() == "" else None)
    black3=tk.Frame(register_window, width=295, height=2, bg='black')
    black3.place(x=25,y=107)

    # Entry field for email
    email = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    email.place(x=30, y=150)
    email.insert(0, 'Enter your Email')
    #email.bind('<FocusIn>', lambda e: email.delete(0, 'end'))
    #email.bind('<FocusOut>', lambda e: email.insert(0, 'Enter your Email') if email.get() == "" else None)
    black4=tk.Frame(register_window, width=295, height=2, bg='black')
    black4.place(x=25,y=177)

   # Entry field for PHONE NUMBER
    phone_number = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    phone_number.place(x=30, y=210)
    phone_number.insert(0, 'Enter your Phone Number')
    #phone_number.bind('<FocusIn>', lambda e: phone_number.delete(0, 'end'))
    #phone_number.bind('<FocusOut>', lambda e: phone_number.insert(0, 'Enter your Phone Number') if phone_number.get() == "" else None)
    black5=tk.Frame(register_window, width=295, height=2, bg='black')
    black5.place(x=25,y=240)

    # Entry field for NATIONAL ID
    national_id = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    national_id.place(x=30, y=270)
    national_id.insert(0, 'Enter your National ID')
    #national_id.bind('<FocusIn>', lambda e: national_id.delete(0, 'end'))
    #national_id.bind('<FocusOut>', lambda e: national_id.insert(0, 'Enter your National ID') if national_id.get() == "" else None)
    black6=tk.Frame(register_window, width=295, height=2, bg='black')
    black6.place(x=25,y=310)

    #Add user button
    add_user_btn = tk.Button(register_window, width=39, pady=7, text="Register User", \
        bg='#57a1f8' ,fg='white', cursor="hand2" ,border=0, \
            command= lambda: add_user(account_number.get(), email.get(), national_id.get(), phone_number.get()))
    add_user_btn.grid(row=2, column=1, sticky="E")
    add_user_btn.place(x=35,y=350)

    #Have an account? login
    label=tk.Label(register_window,text="Already have an account?" , \
    fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=75,y=400)

    signedIn_btn=tk.Button(register_window, text='Login', width=6, fg='#57a1f8', border=0, bg='white', cursor='hand2',command=on_login_click)
    signedIn_btn.place(x=215, y=400)

    # Add the new user to the database
    def add_user( phone_number, account_number, national_id, email):

        sql = "INSERT INTO account_info (account_number, email, phone_number, national_ID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (email.get(), account_number.get(), national_id.get(), phone_number.get()))

        print(account_number)
        #commit changes
        conn.commit()

        #close connection and cursor
        conn.close()
        cursor.close

    register_window.mainloop()



def on_enter_login(e):
    login_button['background'] = '#57a1f8'

def on_leave_login(e):
    login_button['background'] = 'SystemButtonFace'

def on_enter_signup(e):
    signup_button['background'] = '#57a1f8'

def on_leave_signup(e):
    signup_button['background'] = 'SystemButtonFace'

root = tk.Tk()
root.title('ATM system')
root.geometry("925x500+300+200")
root.configure(bg='#fff')
root.resizable(False,False)

land_label= tk.Label(root, text='Welcome to Chase Bank', bg='white', \
    fg='black', font=("Helvetica", 16))
land_label.pack(pady=20)


login_button = tk.Button(root, text='Login', width=39, pady=7, bd=0, height=2, cursor="hand2", \
    command=on_login_click)
login_button.pack(pady=20)
login_button.bind("<Enter>", on_enter_login)
login_button.bind("<Leave>", on_leave_login)

signup_button = tk.Button(root, text='Signup', width=39, pady=7, bd=0, height=2, \
    cursor="hand2", command=on_signup_click)
signup_button.pack(pady=20)
signup_button.bind("<Enter>", on_enter_signup)
signup_button.bind("<Leave>", on_leave_signup)


root.mainloop()



