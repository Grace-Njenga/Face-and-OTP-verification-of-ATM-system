from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import pymysql.cursors
from datetime import datetime, timedelta
import requests
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pdfkit
import tempfile


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

        # Get the current date and time
        now = datetime.now()
        expiry = now + timedelta(seconds=60)
        print("OTP expires at:",expiry)

        sql = "UPDATE account_info SET otp_expiry=%s WHERE account_number=%s"
        cursor.execute(sql, (expiry, account_number))

        query = "UPDATE account_info SET login_time =%s WHERE account_number= %s"
        cursor.execute(query, (now, account_number))
        
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
        #add code to verify if account number exists in database
        # and display an appropriate message box
            
    #verify and open dashboar for either withdrawal or deposit
    def verify_otp(self):
        user_otp = self.otp_entry.get()

        if int(user_otp) == self.otp:
            connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
            #check if account number is valid
            cursor = connection.cursor()
            account_number = self.acct_num_entry.get()
            #verify account number exists in the databse
            query = "SELECT otp_expiry FROM account_info WHERE account_number=%s"
            cursor.execute(query, (account_number,))
            result = cursor.fetchone()[0]

            # check if the OTP has expired
            current_time = datetime.now()
            print(current_time,"Your current time")
            #tup_current= tuple(current_time)
            if result < current_time:
                messagebox.showerror("ERROR", "OTP Expired")
            else:
                messagebox.showinfo("Success", "OTP verified successfully")
                #DashBoard(self.master)
                self.Dash_Board()
        else:
            messagebox.showerror("Error", "Invalid OTP")
    
    #open withdraw and deposit windows
    def Dash_Board(self):
        #super().__init__(master)
        dash = Toplevel(self.master)
        dash.title("CHASE Banking ATM")
        dash.geometry("925x500+300+200")
        dash.configure(bg='white')
        #create two buttons for login and deposit initialize function when both are clicked
        # Add widgets and layout
        connection = pymysql.connect(host='localhost',
                                  user='NJENGA',
                                  passwd='mynewpass',
                                  database='atm')
        account_no = self.acct_num_entry.get()
        query = f"SELECT balance FROM account_info WHERE account_number = {account_no}"
        cursor = connection.cursor()
        cursor.execute(query)
        result=cursor.fetchone()[0]

        Label(dash, bg='white', width=30, font=("Taviraj, bolder", 10), text=f"{account_no} \nYOUR BALANCE IS: KSHS {result}").pack(pady=20)
        withdraw_button = Button(dash, text='Withdraw', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                                   command=self.withdraw)
        deposit_button = Button(dash, text='Deposit', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                                   command=self.deposit)
        history_button = Button(dash, text='History', width=20, height=2, bd=0, bg='#57a1f8', fg='white',
                                   command=self.show_history)       
        withdraw_button.pack(pady=20)
        deposit_button.pack(pady=20)
        history_button.pack(pady=20)

        # Create a Logout button
        self.logout_button = tk.Button(dash, text="Logout", font=("Muli", 10),width=20, height=2, bd=0, bg='red', fg='white', command=self.logout)
        self.logout_button.pack(side="left", padx=15)

    # Logout function to close all windows except main window
    def logout(self):
    # destroy all windows except main window
        for window in self.master.winfo_children():
            if window != self.master:
                window.destroy()

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        History(history_window)

    def withdraw(self):
        connection = pymysql.connect(host='localhost',
                                  user='NJENGA',
                                  passwd='mynewpass',
                                  database='atm')

        account_no = self.acct_num_entry.get()
        query = f"SELECT balance FROM account_info WHERE account_number = {account_no}"
        with connection.cursor() as cursor:
            cursor.execute(query)
            #check balance in database
            balance = cursor.fetchone()[0]

        if balance == 0 :
            messagebox.showerror("Error","Insufficient Funds")
            #self.DashBoard()
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
        #get phone number previously entered
        simu = self.phone_number
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
        print (result)
        #bal = int(result)

        new_balance = result - withdrawal_int
        # Add the deposit amount to the balance
        new_balance = result - withdrawal_int
        whack_query= "UPDATE account_info SET balance = %s WHERE account_number =%s"
        cursor.execute(whack_query, (new_balance, account_no))

        #withdraw time 
        with_time = datetime.now()
        sql = "UPDATE account_info SET Withdraw_time = %s WHERE account_number = %s"
        cursor.execute(sql,(with_time,account_no))

        #get login_time
        cursor.execute(f"SELECT login_time FROM account_info WHERE account_number = '{account_no}'")
        log = cursor.fetchone()[0]

        #update the transaction history
        cursor.execute("INSERT INTO transaction_history (account_number, transaction_date,transaction_type, transaction_amount, login_time) VALUES (%s, %s,%s, %s,%s)", (account_no, with_time,"Withdraw", withdrawal, log))

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
                    "mobile": [simu],
                    "msg": f"Your have successfully withdrawed Kshs:{withdrawal}.Your new balance is Kshs:{new_balance}"
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            ## Display a message to the user
            messagebox.showinfo("Deposit", f"Withdrawal of {withdrawal} successful. New balance: {new_balance}")
        else:
            messagebox.showerror("Error", "Recharge HPK")
        print(response.content)
        connection.commit()
        connection.close()
    
    
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
        #get phone number previously entered
        simu = self.phone_number
        #deposit entry get
        deposition = self.insertion_entry.get()
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

        #deposit time
        deposit_time = datetime.now()
        sql2 = "UPDATE account_info SET deposit_time = %s WHERE account_number = %s"
        cursor.execute(sql2, (deposit_time, account_no))

        whack_query= "UPDATE account_info SET balance = %s WHERE account_number =%s"
        cursor.execute(whack_query, (new_balance, account_no))

        #get login_time
        cursor.execute(f"SELECT login_time FROM account_info WHERE account_number = '{account_no}'")
        now = cursor.fetchone()[0]

        #update the transaction history
        cursor.execute("INSERT INTO transaction_history (account_number, transaction_date, transaction_type, transaction_amount, login_time) VALUES (%s, %s,%s, %s, %s)", (account_no, deposit_time,"Deposit", deposition, now))

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
                    "mobile": [simu],
                    "msg": f"Your have successfully deposited Kshs:{deposition}.Your new balance is Kshs:{new_balance}"
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            ## Display a message to the user
            messagebox.showinfo("Deposit", f"Deposit of {deposition} successful. New balance: {new_balance}")
            print("You have withdrawed:"+str(deposition))
        else:
            messagebox.showerror("Error", "Recharge HPK")
        print(response.content)

        connection.commit()
        ## Display a message to the user
        messagebox.showinfo("Deposit", f"Deposit successful. New balance: {new_balance}")

    #get account entry 
    def account_number(self):
        account_no = self.acct_num_entry.get()
        return account_no

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
        self.email_entry.pack(pady=1)
        #black line widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=5)

        # create entry field for phone number
        self.digits_label = Label(master, text="Your phone Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.digits_label.pack(pady=20)
        #entry widget
        self.digits_entry = Entry(master, bd=0,width=25)
        self.digits_entry.pack(pady=1)
        #blackline frame widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=5)

        
        # create entry field for national ID
        self.national_label = Label(master, text="Your National ID Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.national_label.pack(pady=20)
        #entry widget for id
        self.national_entry = Entry(master, width=25, bd=0)
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
                    "mobile": [phone_no],
                    "msg": f"Welcome, Your CHASE BANK account number is {account_number}"
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            messagebox.showinfo("Account Number", "Your account number has been sent")
        else:
            messagebox.showerror("Error", "Failed to save to database")
        print(response.content)
        print("Your account number is:"+str(account_number))

        #show their new account number
        messagebox.showinfo("YOUR ACCOUNT NUMBER",f"Your Chase Bank Account number is: {account_number}")
        print('successful insertion of detais into table')

        connection.commit()

#history of either withdrawal or deposit
class History():#login
    def __init__(self, master):
        #super().__init__(master)
        self.master = master
        master.title ("C H A S E  B A N K")
        master.geometry("925x500+300+200")
        master.configure(bg='white')

        Label(master, bg='white', width=30, font=("Taviraj, bolder", 10), text="TRANSACTION HISTORY").pack(pady=20)
        
        self.acct_num_label = Label(master, text="Enter Account Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.acct_num_label.pack(pady=20)

        #Entry widget
        self.acct_num_entry = Entry(master, width=25, bd=0 )
        self.acct_num_entry.pack(pady=1)

        #black line widget
        self.black = Frame(master, width=295, height=2, bg='black')
        self.black.pack(pady=5)#x=25,y=107

        # create button to verify account number
        self.verify_button = Button(master, text="Show History", bg='#57a1f8', height=2, bd=0, width=30, cursor='hand2', fg="white", font=('Taviraj'), command=self.show_hist)
        self.verify_button.pack(pady=20)

        Button(master, text="EXIT", bg='red', height=2, bd=0, width=30, cursor='hand2', fg="white", font=('Taviraj'), command=self.close_window).pack(pady=20)

    def show_hist(self):
        if hasattr(self, 'history_win'): # check if the window already exists
            self.history_win.destroy() # destroy the previous window if it exists
        history_win = Toplevel(self.master)
        history_win.title("TRANSACTION HISTORY")
        history_win.geometry("925x500+300+200")
        history_win.configure(background='white')

        # Get the account number from the Login class
        account_number = self.acct_num_entry.get()

        Label(history_win, bg='white', width=30, font=("Muli, bolder", 10), text=f"Transaction history for account:{account_number}").pack(pady=20)

        # Create a treeview widget to display the transaction history
        self.tree = ttk.Treeview(history_win, columns=('date', 'type', 'amount', 'time'), selectmode='browse')
        self.tree.heading('#0', text='Transaction ID')
        self.tree.heading('date', text='Date')
        self.tree.heading('type', text='Type')
        self.tree.heading('amount', text='Amount')
        self.tree.heading('time', text='Login Time')
        self.tree.pack(pady=20)

        # Query the database for transaction history
        connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
        cursor = connection.cursor()
        query = f"SELECT transaction_id, transaction_date, transaction_type, transaction_amount, login_time FROM transaction_history WHERE account_number = '{account_number}'"
        cursor.execute(query)
        results = cursor.fetchall()

        # Populate the treeview with the transaction history
        for row in results:
            self.tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4]))

        Button(history_win, text="Send to email", bg='#57a1f8', height=2, bd=0, width=30, cursor='hand2', fg="white", font=('Taviraj'), command = self.send_transaction_history).pack(pady=20)

        # Create a button to go back to the dashboard
        def go_to_dashboard():
            history_win.destroy()

        Button(history_win, text="back", bg='#57a1f8', height=2, bd=0, width=30, cursor='hand2', fg="white", font=('Taviraj'), command=go_to_dashboard).pack(pady=20)

    #send the table to user's email
    def send_transaction_history(self):
        # Get the account number from the Login class
        account_number = self.acct_num_entry.get()

        # Query the database for transaction history
        connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
        cursor = connection.cursor()

        #get users email based on their account_number
        email = "SELECT email FROM account_info WHERE account_number = %s"
        cursor.execute(email,(account_number,))
        email_address = cursor.fetchone()
        print(email_address)

        query = f"SELECT transaction_id, transaction_date, transaction_type, transaction_amount, login_time FROM transaction_history WHERE account_number = '{account_number}'"
        cursor.execute(query)
        results = cursor.fetchall()

        # Create a string with the transaction history
        transaction_history = "Transaction history:\n"
        for row in results:
            transaction_history += f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n"

        # Create a multipart message and set the subject, from, to and attachment
        message = MIMEMultipart()
        message['Subject'] = 'Transaction History'
        message['From'] = 'Nyamburanjenga3482@outlook.com'
        message['To'] = str(email_address)

        # Attach the transaction history table as a text file
        attachment = MIMEText(transaction_history)
        attachment.add_header('Content-Disposition', 'attachment', filename='transaction_history.txt')
        message.attach(attachment)

        # Set up an SMTP connection to the Outlook server and send the email
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('Nyamburanjenga3482@outlook.com', 'Gr7,ace.')
            smtp.sendmail('Nyamburanjenga3482@outlook.com', email_address, message.as_string())

        # Show a message box to indicate that the email was sent successfully
        messagebox.showinfo("Email Sent", "Transaction history email sent successfully!")
    
    #close history class and back to login class
    def close_window(self):
        self.master.destroy()  
#face recognition class

root = Tk()
my_gui = Login(root)
root.mainloop()
