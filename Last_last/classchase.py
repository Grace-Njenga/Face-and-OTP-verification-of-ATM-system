from tkinter import *
from tkinter import messagebox
import random
import pymysql
import requests
import json

#class function for login that includes otp,account verification and deposit or withdraw
class BankingApp:
    def __init__(self, master):
        self.master = master
        master.title("Banking App")
        master.geometry("925x500+300+200")
        master.configure(bg='white')
        
        # create entry field for account number
        self.acct_num_label = Label(master, text="Account Number:", bg='white', font=('Pragati Narrow, bold',12))
        self.acct_num_label.pack()
        self.acct_num_entry = Entry(master)
        self.acct_num_entry.pack(pady=10)

        # create button to verify account number
        self.verify_button = Button(master, text="Send OTP", bg='#57a1f8', height=2, width=30, cursor='hand2', fg="white", font=('Taviraj'), command=self.verify_acct_num)
        self.verify_button.pack()

    def send_otp(self):
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
            messagebox.showinfo("OTP Sent", "An OTP has been sent to your phone")
        else:
            messagebox.showerror("Error", "Failed to send OTP")
        print(response.content)
    #    # replace <API_KEY> with your actual API key from the textlocal website
    #    #response = requests.get('https://api.textlocal.in/send/?#apikey=<API_KEY>&numbers=' + str(self.#phone_number)
    #    #                        + '&message=Your%20OTP%20is%20' #+ str(self.otp) + '.')
    #    #print(response.content)

    def verify_acct_num(self):
        account_number = self.acct_num_entry.get()
        connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
        #check if account number is valid
        cursor = connection.cursor()
        #verify account number exists in the databse
        query = "SELECT * FROM account_info WHERE account_number=%s"
        cursor.execute(query, (account_number,))
        account = cursor.fetchone()
        #if no result is found show error
        if not account:
            messagebox.showerror("Error", "Invalid account  number.")
        else:
            self.phone_number = account[4]
            self.otp = random.randint(1000, 9999)
            self.send_otp()
            otp_window = Toplevel(self.master)
            otp_window.title("OTP Verification")
            otp_window.geometry("460x250+150+100")
            otp_window.configure(background='white')

            Label(otp_window, text="Enter sent OTP", bg='white', width=30, font=("Taviraj,bold", 10)).pack()
            self.otp_entry = Entry(otp_window)
            self.otp_entry.pack()

            verify_button = Button(otp_window, text='Verify OTP', width=20, height=2, bg='#57a1f8', fg='white',
                                   command=self.verify_otp)
            verify_button.pack(pady=20)
        # TODO: add code to verify if account number exists in database
        # and display an appropriate message box
    def verify_otp(self):
        user_otp = self.otp_entry.get()

        if int(user_otp) == self.otp:
            messagebox.showinfo("Success", "OTP verified successfully")
            print("OTP correct")
            # fetch account balance from db and open the dashboard
            connection = pymysql.connect(host='localhost',
                                     user='NJENGA',
                                     passwd='mynewpass',
                                     database='atm')
            cursor = connection.cursor()

            account_no = self.acct_num_entry.get()
            query = f"SELECT balance FROM users WHERE account_number = {account_no}"
            cursor.execute(query)

            balance = cursor.fetchone()[0]
            print(f"Account balance is {balance}")

            dashboard_window = Toplevel(self.master)
            dashboard_window.title("Dashboard")
            dashboard_window.geometry("925x500+300+200")
root = Tk()
my_gui = BankingApp(root)
root.mainloop()
