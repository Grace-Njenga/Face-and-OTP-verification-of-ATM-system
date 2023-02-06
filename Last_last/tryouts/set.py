from tkinter import *
from tkinter import messagebox
from tkinter import ttk

root= Tk()

#window title
root.title('LOGIN AND REGISTRATION')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False,False)

def signin():
    account=acc.get()
    email=ema.get()

    if account=='' and email =='':
         messagebox.showerror('ERROR', 'Fields cannot be empty')
    


##################IMAGE######################################################################################
img = PhotoImage(file='login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg= 'white')
frame.place(x=480, y=70)

title_label=Label(frame, text='LOG IN', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
title_label.place(x=100, y=5)
############################################################################################################

#account number and Email defined
    #account number and Email
def on_enter(e):
    acc.delete(0, 'end')

def on_leave(e):
    name=acc.get()
    if name =='':
        acc.insert(0, 'Your Account Number') 

acc= Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
acc.place(x=30, y=80)
acc.insert(0, 'Enter account number')
acc.bind('<FocusIn>', on_enter)
acc.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25,y=107)
#################################################################

#Email defined
    #Email
def on_enter(e):
    ema.delete(0, 'end')

def on_leave(e):
    name=ema.get()
    if name =='':
        ema.insert(0, 'Your Email ')

ema= Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
ema.place(x=30, y=150)
ema.insert(0, 'Enter your email')
ema.bind('<FocusIn>', on_enter)
ema.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25,y=177)
#################################################################

#dont have account button
Button(frame, width=39, pady=7,text='SIGN IN' \
    ,bg='#57a1f8' ,fg='white',border=0, command ='signin' ).place(x=35,y=204)
label=Label(frame,text="Don't have an account?" \
    ,fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

sign_up=Button(frame, text='Sign Up', width=6, fg='#57a1f8', border=0, bg='white', cursor='hand2', )
sign_up.place(x=215, y=270)

root.mainloop()
