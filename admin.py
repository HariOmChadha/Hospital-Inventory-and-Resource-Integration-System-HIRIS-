import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv
import sys

#funciton to logout. Exits because multiple windows could be open
def logout():
    messagebox.showinfo("Log out", "Thank you for using our service!")
    sys.exit()

#adds the medicine to the csv file
def medicineCheck():
    #checks the for duplicate medicine name
    check = True
    for i in range (len(data[0])):
        if medicine_name.get() == data[0][i] or medicine_name.get() == "":
            messagebox.showerror("Error", "This medicine either already exists in the database ot is an invalid input")
            medicine_name.delete(0, "end")
            check = False
            break
    if check:
    #creates a new column and overites the old csv
        messagebox.showinfo("Info", "The window will reload now. Please give it a few seconds.")
        df = pd.read_csv("hospital_inventories.csv",  index_col = 0)
        df[medicine_name.get()] = 0
        df.to_csv("hospital_inventories.csv")

        #destroys the windows and opens the new database
        medicineFrame.destroy()
        adminFrame.destroy()
        createMenu()
    return

#adds a new medicine to the database
def addMedicine():
    #creates the window
    global medicineFrame
    medicineFrame = tk.Tk(className = "add medicine")
    medicineFrame.geometry("300x300+400+300")

    #creates the label
    medicine_label = tk.Label(medicineFrame, text = "Please type the name of\nthe medicine that you would like to add:", anchor = "center", pady = 70)
    medicine_label.pack()

    #add the text box
    global medicine_name
    medicine_name = tk.Entry(medicineFrame, justify = "center")
    medicine_name.place(x = 90, y = 125)

    #adds the submit button button
    submit_button = tk.Button(medicineFrame, activeforeground="blue", text = "Submit", command = medicineCheck)
    submit_button.pack()
    
    medicineFrame.mainloop()
    return


#creates the admin window
def createMenu():
    global adminFrame
    #creates the frame
    adminFrame = tk.Tk(className="Admin portal")
    adminFrame.geometry("1100x700+150+50")

    #creates the label at the top
    label1 = tk.Label(text="The current database has the following information:")
    label1.pack(pady = 30)

    #creates a frame to hold the canvas
    Frame1 = tk.Frame(adminFrame, height = 550, width = 800)
    Frame1.place(x = 150, y = 70, height = 550, width = 800)

    #creates canvas inside the frame
    dataCanvas = tk.Canvas(Frame1, height = 500, width = 800)
    dataCanvas.place(anchor = "nw")

    #creates another frame inside the canvas to hold the data
    dataFrame = tk.Frame(dataCanvas)

    #read the csv file and creates a table to display
    reader = csv.reader(open("hospital_inventories.csv"))
    global data
    data = list(reader)
    
    #puts all the data in the dataFrame
    yLength = 0
    xLength = len(data[0])*70
    for row in range(100):    
        for col in range(len(data[row])):
            tk.Label(dataFrame, text= data[row][col]).grid(row = row, column = col)
        yLength += 21
        
    dataCanvas.create_window(0,0,window = dataFrame, anchor = "nw")

    #creates scrollbars to make the data scrollable
    y = tk.Scrollbar(Frame1, orient= "vertical", command = dataCanvas.yview)
    y.pack(side = "right", fill = "y")
    x = tk.Scrollbar(Frame1, orient= "horizontal", command = dataCanvas.xview)
    x.pack(side = "bottom", fill = "x")

    #connects the scrollwheels to the canvas
    dataCanvas.config(yscrollcommand = y.set, xscrollcommand = x.set, scrollregion=(0,0,xLength,yLength))

    #creates the buttons at the bottom to add/remove rows/columns
    #add medicine button
    global medicine_button
    medicine_button = tk.Button(adminFrame, activeforeground="blue", text = "Add medicine", command = addMedicine)
    medicine_button.place(x = 500, y = 650)

    #creates a logout button
    logout_button = tk.Button(adminFrame, activeforeground="blue", text = "Logout", command = logout)
    logout_button.place(x = 700, y = 650)

    adminFrame.mainloop()
    return


