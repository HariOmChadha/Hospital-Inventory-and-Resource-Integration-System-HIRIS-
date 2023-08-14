import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv
import menu
import admin
import sys


#hospitals is the database
hospitals = list(csv.reader(open('can_hospitals_ab.csv')))

#checks if the login information is correct or not
def loginCheck():
    try:
        found  = False
        for i in range (len(hospitals)):
            if hospitals[i][0] == login_code.get():
                global hospitalName
                global code
                found = True
                hospitalName = hospitals[i][1]
                code = int(login_code.get())
                loginFrame.destroy()
                menu.createMenu(hospitalName, code)
                return
        if int(login_code.get()) == 999990:
                found = True
                messagebox.showinfo("Info", "The window will reload now. Please give it a few seconds.")
                loginFrame.destroy()
                admin.createMenu()
                return
        if not found:
            messagebox.showerror("Incorrect Code", "The login code is incorrect. Please try again")
            login_code.delete(0, "end")
    except:
        try:
            if not found:
                if int(login_code.get()) == 999990:
                    loginFrame.destroy()
                    admin.createMenu()
        except:
            if not found:
                messagebox.showerror("Incorrect Code", "The login code is incorrect. Please try again")
                login_code.delete(0, "end")
    return

def close():
    sys.exit()

def createLogin():
    global loginFrame
    global login_code
    #creates the login window
    loginFrame = tk.Tk(className= "Login Screen")
    loginFrame.geometry("300x250+500+200")

    #adds the label that asks to login
    login_label = tk.Label(loginFrame, text = "Welcome to\n Hospital Inventory and Resource Integration System\n(HIRIS)\n\nPlease use your 5 digit code to login:", anchor = "center", pady = 20)
    login_label.pack()

    #add the text box
    login_code = tk.Entry(loginFrame, width = 17, justify = "center")
    login_code.place(x = 100, y = 115)

    #adds the login button
    login_button = tk.Button(loginFrame, activeforeground="blue", text = "Login", command = loginCheck)
    login_button.place(x = 125, y = 150)

    #exit if the main login window is closed
    loginFrame.protocol("WM_DELETE_WINDOW", close)

    loginFrame.mainloop()


if __name__ == '__main__':
    createLogin()