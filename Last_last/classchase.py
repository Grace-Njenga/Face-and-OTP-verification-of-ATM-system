from tkinter import *
import tkinter as tk
from tkinter import messagebox
import random
#import datetime
#import json
import requests
import pymysql

connection = pymysql.connect(host='localhost', user='myuser', password='mypassword', db='mydatabase')
#root class that contains two buttons 
class BankingApp:
    def __init__(self, master):
        self.master = master
        master.title ("C H A S E  B A N K")
        master.geometry("925x500+300+200")
        master.configure(bg='white')

        #widgets that is buttons login and sign in
         # create entry field for account number
        self.landing_label = Label(master, text="Welcome to Chase Bank ATM", bg='white', font=('Pragati Narrow, bold',16))
        self.landing_label.pack( pady=50)

        # create login button
        self.login_button = Button(master, text="Login", bg='#57a1f8', height=2, width=30, bd=0, cursor='hand2', fg="white", font=("Taviraj,bold",13), command=self.open_login)#command=login(self)
        self.login_button.pack(pady=20)

         # create signin button
        self.signin_button = Button(master, text="Signin", bg='#57a1f8', height=2, width=30, bd=0, cursor='hand2', fg="white", font=('Taviraj, bold', 13), command=self.open_signin)#, command=register(self)
        self.signin_button.pack(pady=20)
    
    def open_login(self):
        login_window = tk.Toplevel(self.master)
        Login(login_window)
    
    def open_signin(self):
        signin_window = tk.Toplevel(self.master)
        Register(signin_window)


#class function for login that includes otp,account verification and deposit or withdraw
class Login:
    def __init__(self, master):
        self.master = master
        master.title("CHASE Banking ATM")
        master.geometry("925x500+300+200")
        master.configure(bg='white')
        
        #label for the window
        self.landing_label = Label(master, text="Enter your account number for login", bg='white', font=('Pragati Narrow, bold',16))
        self.landing_label.pack( pady=30)

        # create entry field for account number
        self.acct_num_label = Label(master, text="Enter Account Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.acct_num_label.pack(pady=20)

        #Entry widget
        self.acct_num_entry = Entry(master, width=25, bd=0 )
         #placeholder widget
        #self.acct_num_entry.insert(0,"Enter your account no")
        #self.acct_num_entry.bind('<FocusIn>', lambda e: self.acct_num_entry.delete(0, 'end'))
        #self.acct_num_entry.bind('<FocusOut>')#, lambda e: self.acct_num_entry.insert(0, 'Enter Account Number', fg='blue')
        self.acct_num_entry.pack(pady=1)

        #black line widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=5)#x=25,y=107

        # create button to verify account number
        self.verify_button = Button(master, text="Send OTP", bg='#57a1f8', height=2, bd=0, width=30, cursor='hand2', fg="white", font=('Taviraj'), command=self.verify_acct_num)
        self.verify_button.pack(pady=20)

    def send_otp(self):
        #conect to database to save the enetered/sent otp
        connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
        cursor = connection.cursor()

        account_number = self.acct_num_entry.get()
        otp = self.otp
        #otp_expiry = self.otp_expiry

        #stores the otp into the database
        query = "UPDATE account_info set otp= %s WHERE account_number = %s"
        cursor.execute(query, (otp, account_number))

        #saves the otp into the database
        connection.commit()

        #hostpinnacle API for SMS BULK
        url = "https://smsportal.hostpinnacle.co.ke/SMSApi/send"
        headers = {"Content-Type": "application/json"}
        data = {
            "userid": "Nyambura",
            "password": "9kgEQkc0",
            "senderid": "HPKSMS",
            "msgType": "text",
            "duplicatecheck": "true",
            "sendMethod": "quick",
            "sms": [
                {
                    "mobile": [self.phone_number],
                    "msg": f"Your OTP is {self.otp}"
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            messagebox.showinfo("OTP Sent", "An OTP has been sent.")
        else:
            messagebox.showerror("Error", "Failed to send OTP")
        print(response.content)
        print("Your otp is:"+str(otp))

    def verify_acct_num(self):
        
        connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
        #check if account number is valid
        cursor = connection.cursor()
        account_number = self.acct_num_entry.get()
        #verify account number exists in the databse
        query = "SELECT phone_number FROM account_info WHERE account_number=%s"
        cursor.execute(query, (account_number,))
        mobile_number = cursor.fetchone()
        #if no result is found show error
        if not mobile_number:
            messagebox.showerror("Error", "Invalid account  number.")
        else:
            self.phone_number = mobile_number[0]
            self.otp = random.randint(1000, 9999)
            self.send_otp()
            otp_window = Toplevel(self.master)
            otp_window.title("OTP Verification")
            otp_window.geometry("460x250+150+100")
            otp_window.configure(background='white')

            Label(otp_window, text="Enter sent OTP", bg='white', width=30, font=("Taviraj,bold", 10)).pack(pady=20)
            #entry widget
            self.otp_entry = Entry(otp_window, width=25, bd=0)
            self.otp_entry.pack(pady=1)
             #black line widget
            self.black = Frame(otp_window, width=295, height=2, bg='black')
            self.black.pack(pady=5)#x=25,y=107

            verify_button = Button(otp_window, text='Verify OTP', bd=0, width=20, height=2, bg='#57a1f8', fg='white',
                                   command=self.verify_otp)
            verify_button.pack(pady=20)
        # TODO: add code to verify if account number exists in database
        # and display an appropriate message box

        
    #verify and open dashboar for either withdrawal or deposit
    def verify_otp(self):
        user_otp = self.otp_entry.get()

        if int(user_otp) == self.otp:
            messagebox.showinfo("Success", "OTP verified successfully")
            print("OTP correct")
            self.DashBoard()
        else:
            messagebox.showerror("Error", "Invalid OTP")   

    #open withdraw an deposit windows
    def DashBoard(self):
        dash = Toplevel(self.master)
        dash.title("CHASE Banking ATM")
        dash.geometry("925x500+300+200")
        dash.configure(bg='white')

        #create two buttons for login and deposit initialize function when both are clicked
        # Add widgets and layout
        withdraw_button = Button(dash, text='Withdraw', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                                   command=self.withdraw)
        deposit_button = Button(dash, text='Deposit', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                                   command=self.deposit)
        
        withdraw_button.pack(pady=20)
        deposit_button.pack(pady=20)
        ...

    def withdraw(self):
        #WithdrawWindow(self.master)
        connection = pymysql.connect(host='localhost',
                                  user='NJENGA',
                                  passwd='mynewpass',
                                  database='atm')
        cursor = connection.cursor()
        account_no = self.acct_num_entry.get()
        query = f"SELECT balance FROM account_info WHERE account_number = {account_no}"
        cursor.execute(query)
        #check balance in database
        balance = cursor.fetchone()
        print(f"Account balance is {balance}")
        if balance is None :
            messagebox.showerror("Error","Insufficient Funds")
        else:
            toa = Toplevel(self.master)
            toa.title("WITHDRAW")
            toa.geometry("460x250+150+100")
            toa.configure(background='white')

            Label(toa, text="Enter amount to withdraw", bg='white', width=30, font=("Taviraj,bold", 10)).pack()
            self.with_entry = Entry(toa)
            self.with_entry.pack()

            verify_button = Button(toa, text='Withdraw', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                                   command=self.database_change)
            verify_button.pack(pady=20)

    #minus the amount etered in the database
    def database_change(self):
        #get accout number previously entered
        account_no = self.acct_num_entry.get()
        #get the deposit entry
        withdrawal = self.with_entry.get()
        #convert into integer
        withdrawal_int = int(withdrawal)

        #connect to the database
        connection = pymysql.connect(host='localhost',
                                  user='NJENGA',
                                  passwd='mynewpass',
                                  database='atm')
        cursor = connection.cursor()
        #update the database by getting the account number
        query = f"SELECT balance FROM account_info WHERE account_number = '{account_no}'"
        cursor.execute(query)
        #check balance in database
        result = cursor.fetchone()[0]
        #bal = int(result)

        # Add the deposit amount to the balance
        new_balance = result - withdrawal_int
        # Update the balance in the database
        print("Your new balance is " + str(new_balance))
        print("Your previous balance was " +str(result))

        print(account_no)
        whack_query= "UPDATE account_info SET balance = %s WHERE account_number =%s"
        cursor.execute(whack_query, (new_balance, account_no))
        connection.commit()
        ## Display a message to the user
        messagebox.showinfo("Deposit", f"Withdrawal of {withdrawal} successful. New balance: {new_balance}")

    def deposit(self):
        connection = pymysql.connect(host='localhost',
                                  user='NJENGA',
                                  passwd='mynewpass',
                                  database='atm')
        cursor = connection.cursor()
        account_no = self.acct_num_entry.get()
        query = f"SELECT balance FROM account_info WHERE account_number = {account_no}"
        cursor.execute(query)
        #check balance in database
        balance = cursor.fetchone()
        print(f"Account balance is {balance}")
        
        weka = Toplevel(self.master)
        weka.title("WITHDRAW")
        weka.geometry("460x250+150+100")
        weka.configure(background='white')

        Label(weka, text="Enter amount to deposit", bg='white', width=30, font=("Taviraj,bold", 10)).pack()
        self.insertion_entry = Entry(weka)
        self.insertion_entry.pack()
        verify_button = Button(weka, text='deposit', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                               command=self.install)
        verify_button.pack(pady=20)

    #database action once  button is clicked
    def install(self):
        #get accout number previously entered
        account_no = self.acct_num_entry.get()
        #get the deposit entry
        deposit = self.insertion_entry.get()
        #convert into integer
        deposit_int = int(deposit)

        #connect to the database
        connection = pymysql.connect(host='localhost',
                                  user='NJENGA',
                                  passwd='mynewpass',
                                  database='atm')
        cursor = connection.cursor()
        #update the database by getting the account number
        query = f"SELECT balance FROM account_info WHERE account_number = '{account_no}'"
        cursor.execute(query)
        #check balance in database
        result = cursor.fetchone()[0]
        #bal = int(result)

        # Add the deposit amount to the balance
        new_balance = result + deposit_int
        # Update the balance in the database
        print(account_no)
        print("Your new balance is " + str(new_balance))
        print("Your previous balance was " +str(result))
        whack_query= "UPDATE account_info SET balance = %s WHERE account_number =%s"
        cursor.execute(whack_query, (new_balance, account_no))
        connection.commit()
        ## Display a message to the user
        messagebox.showinfo("Deposit", f"Deposit successful. New balance: {new_balance}")
            

#CLass for signup button
class Register:
    def __init__(self, master):
        self.master = master
        master.title ("C H A S E  B A N K")
        master.geometry("925x500+300+200")
        master.configure(bg='white')

        #label for the window
        self.land_label = Label(master, text="REGISTRATION", bg='white', font=('Pragati Narrow, bold',16))
        self.land_label.pack()

        # create entry field for email
        self.email_label = Label(master, text="Your Email:", bg='white', font=('Pragati Narrow, bold',12))
        self.email_label.pack(pady=20)
        #entry widget
        self.email_entry = Entry(master, width=25, bd=0)
        #placeholder widget
        #self.email_entry.insert(0,"Enter your email address")
        #self.email_entry.bind('<FocusIn>', lambda e: self.email_entry.delete(0, 'end'))
        #self.email_entry.bind('<FocusOut>', lambda e: self.email_entry.insert(0, 'Enter Account Number'))#
        self.email_entry.pack(pady=1)
        #black line widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=5)

        
        # create entry field for phone number
        self.digits_label = Label(master, text="Your phone Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.digits_label.pack(pady=20)
        #entry widget
        self.digits_entry = Entry(master, bd=0,width=25)
        #placeholder widget
        #self.digits_entry.insert(0,"Write number as 2547xxxxxxxx")
        #self.digits_entry.bind('<FocusIn>', lambda e: self.digits_entry.delete(0, 'end'))
        #self.digits_entry.bind('<FocusOut>', lambda e: self.digits_entry.insert(0, 'Write number as 2547xxxxxxxx'))
        self.digits_entry.pack(pady=1)
        #blackline frame widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=5)

        
        # create entry field for national ID
        self.national_label = Label(master, text="Your National ID Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.national_label.pack(pady=20)
        #entry widget for id
        self.national_entry = Entry(master, width=25, bd=0)
        #placeholder widget
        #self.national_entry.insert(0,"Enter your ID")
        #self.national_entry.bind('<FocusIn>', lambda e: self.national_entry.delete(0, 'end'))
        #self.national_entry.bind('<FocusOut>', lambda e: self.national_entry.insert(0, 'Enter Your National ID'))
        self.national_entry.pack(pady=1)
        #black line frame widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=1)

        #button to ad user to the database and direct them to login class so they can login 
        self.add_button = Button(master, text="Register", bg='#57a1f8', height=2, width=30, bd=0, cursor='hand2', fg="white", font=('Taviraj'), command=self.add_user)
        self.add_button.pack(pady=20)

    #function enters database and gives user an account number, and saves the user into the database
    def add_user(self):
        connection = pymysql.connect(host='localhost',
                              user='NJENGA',
                              passwd='mynewpass',
                              database='atm')
        cursor = connection.cursor()

        email= self.email_entry.get()
        national_id = self.national_entry.get()
        account_number = random.randint(100000000,999999999)
        phone_no = self.digits_entry.get()

        #insert all the fiels into the database
        query = "INSERT INTO account_info (email, account_number, national_ID, phone_number) VALUES (%s, %s, %s, %s)"
        cursor.execute( query, (email, account_number, national_id, phone_no))

        connection.commit()

        #show their new account number
        messagebox.showinfo("YOUR ACCOUNT NUMBER",f"Your Chase Bank Account number is: {account_number}")
        print(f'your account number is {account_number}')
        print('successful insertion of detais into table')

        #class function to be calle after ok button in message box has been clicked and destroy this window so user is taken to login page 

        #login(self)

root = Tk()
my_gui = BankingApp(root)
root.mainloop()
