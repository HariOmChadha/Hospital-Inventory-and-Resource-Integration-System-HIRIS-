import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import csv
import os
import main
from math import sin, cos, atan2, radians, sqrt





#logout sequence
def logout():
    messagebox.showinfo("Log out", "Thank you for using our service!")
    menuFrame.destroy()
    main.createLogin()
    return

#to upload the hospital inventory file
def upload():
    messagebox.showinfo("File Upload", "Please make sure that the file is .csv and follows the defined template.")
    #open file explorer to get the file
    try:
        data = []
        file = filedialog.askopenfile()
        tempData = list(csv.reader(file))  
        for i in range (1,len(tempData)):
            data.append(tempData[i][1])  
    except:
        messagebox.showerror("Error!", "Please make sure that the file is .csv and follows the defined template.")
    #creates the dataframe and updates it and turns it to a csv file again
    df = pd.read_csv("hospital_inventories.csv", index_col="index_code")
    df.loc[key] = data
    os.remove("hospital_inventories.csv")
    df.to_csv("hospital_inventories.csv")
    return

def requestMedicine(num):
    if num > 1:
        result =  messagebox.askquestion("Confirm", "Are you sure you want to request the medicines from this hospital? This is not the most recommened choice.")
        if result == 'yes':
            messagebox.showinfo("Confirmed", "Your request has been confirmed. Thank you!")
            resultFrame.destroy()
            medicine_name.delete(0,"end")
            quantity_entry.delete(0, "end")
            
    else:
        result =  messagebox.askquestion("Confirm", "Are you sure you want to request this medicine?")
        if result == 'yes':
            messagebox.showinfo("Confirmed", "Your request has been confirmed. Thank you!")
            resultFrame.destroy()
            medicine_name.delete(0,"end")
            quantity_entry.delete(0, "end")
    return

def printResults():
    global resultFrame
    optimizeResults()
    #deletes and previous results
    resultFrame.destroy()

    #creates a new frame with the same name
    resultFrame = tk.Frame(menuFrame, height = 550, width = 1000)
    resultFrame.place(x = 200, y = 180, height = 550, width = 800)

    #creates canvas inside the frame
    dataCanvas = tk.Canvas(resultFrame, height = 500, width = 800)
    dataCanvas.place(anchor = "nw")

    #creates another frame inside the canvas to hold the data
    dataFrame = tk.Frame(dataCanvas)

    #read the csv file and creates a table to display
    reader = csv.reader(open("runtime_hospital_scores.csv"))
    global data
    data = list(reader)
    
    #puts all the data in the dataFrame using more frames that have labels and buttons in a grid 
    yLength = 0
    for row in range(1, len(data)): 
        #frame with all the info  
        if key != data[row][0]:
            yLength += 150 

            #button for requesting medicine
            button = tk.Button(dataFrame, activeforeground="blue", text = data[row][1]+ "                Qunatity in stock: " +  data[row][7] + "\nDistance (in kms): " + data[row][4] + "                Delivery time (in minutes): " + str(round(float(data[row][4])/0.8)), justify = "left", font = ("courier", 9), height = 8, width = 100, command = lambda row = row: requestMedicine(row)).grid(row = row, column = 0)
        
    dataCanvas.create_window(0,0,window = dataFrame, anchor = "nw")

    #creates scrollbars to make the data scrollable
    y = tk.Scrollbar(resultFrame, orient= "vertical", command = dataCanvas.yview)
    y.pack(side = "right", fill = "y")
   
    #connects the scrollwheels to the canvas
    dataCanvas.config(yscrollcommand = y.set, scrollregion=(0,0,0,yLength))
    
    return

def optimizeResults():
    hospitals = pd.read_csv("can_hospitals_ab.csv", index_col = 0)
    inventory = pd.read_csv("hospital_inventories.csv", index_col = 0) # Columns of hospital records and rows of items

    index_key = key # sets current hospital
    item =  medicine# sets item to search for
    item_quant = number # number of items needed

    # if index_key not in hospitals.index:
    #     print("Hospital not found")
    # elif item not in inventory.index:
    #     print("Item not found")

    ### Creates measures of metrics to optimize with ###
    measures = pd.DataFrame(columns = ['distance', 'size', 'occupancy', 'quantity'])

    current_hospital = hospitals[['latitude', 'longitude']].loc[index_key]
    cy = radians(current_hospital['latitude'])
    cx = radians(current_hospital['longitude'])

    for other_h_index_code, other_hospital in hospitals.iterrows(): # Checks for mismatch of database indexes
        if other_h_index_code not in inventory.index:
            hospitals.drop(other_h_index_code, axis = 1)
            continue
        
        # Number of inventory objects in other hospital; only continues if stock is more than item_quant
        quantity = inventory.at[other_h_index_code, item]
        if quantity < item_quant:
            continue

        # Distance of other hospital from current hospital; great circle calculation
        oy = radians(other_hospital['latitude'])
        ox = radians(other_hospital['longitude'])
        a = sin((oy-cy)/2)**2 + cos(cy)*cos(oy)*((sin((ox-cx)/2))**2) 
        c = 2 * atan2(sqrt(a),sqrt(1-a))
        distance = 6371*c

        # Total capacity of other hospital
        size = other_hospital['max_capacity']

        # Occupancy of other hospital
        occupancy = other_hospital['current_capacity_percent'] / other_hospital['max_capacity']

        measures.loc[other_h_index_code] = [distance, size, occupancy, quantity] # writes to measures df


    ### Normalization part starts ###
    normalized_measures = pd.DataFrame(columns = measures.columns)
    largests = measures.max()

    for index_code, row in measures.iterrows(): # Goes through rows
        normalized_measures.loc[index_code] = row / largests


    ### Optimization part starts ###
    # normalized_measures are used as weights for determining "which is better"
    # Better if: distance = smaller; size = bigger; occupancy = smaller; quantity = bigger
    scores = pd.DataFrame(columns = ['scores'])
    properties = pd.DataFrame(columns = ['facility_name', 'city', 'province'])

    # Weight parameters | d = distance; s = size, o = occupancy, q = quantity
    wd = -0.9
    ws = 0.3
    wo = -0.7
    wq = 0.3

    for index_code, row in normalized_measures.iterrows():
        scores.loc[index_code] = (wd*row[0] + ws*row[1] + wo*row[2] + wq*row[3]) / 4
        properties.loc[index_code] = [hospitals.loc[index_code, 'facility_name'], hospitals.loc[index_code, 'city'], hospitals.loc[index_code, 'province']]

    ### Output ###
    output = pd.concat([properties, measures, scores], axis = 1)
    output.to_csv("runtime_hospital_scores.csv")
    return

#checks if the medicine exists and if the input is an acceptable value
def searchCheck():
    search = False
    data = list(csv.reader(open("hospital_inventories.csv")))
    for i in range (1, len(data)):
        try:
            if medicine_name.get() == data[0][i]:
                if  int(quantity_entry.get()) > 0:
                    global number
                    global medicine
                    number = int(quantity_entry.get())
                    medicine = medicine_name.get()
                    search = True
                    if number <= int(data[key-9999][i]):
                        messagebox.showinfo("IN STOCK", f"This medicine is currently in stock (quantity = {data[key-9999][i]}). Please use your own supplies before sending a request to another hospital/clinic.")
                        return
                    break
        except:
            messagebox.showerror("Error!", "Inputs are not valid")
            return
    if not search:   
        messagebox.showerror("Error!", "Inputs are not valid")
        return
    printResults()
    return

#creates the window accessed by the hospitals
def createMenu(hospitalName, code):
    global menuFrame
    global name
    global key
    name = hospitalName
    key = code

    #creates the window
    menuFrame = tk.Tk(className = "Menu")
    menuFrame.geometry("1100x700+150+50")

    #placeholder frame
    global resultFrame
    resultFrame = tk.Frame(menuFrame)

    #creating the label with the hospital name
    name_label = tk.Label(menuFrame, text = "Welcome "+ hospitalName + "!", pady = 30)
    name_label.pack()

    #creates a logout button
    logout_button = tk.Button(menuFrame, activeforeground="blue", text = "Logout", command = logout)
    logout_button.place(x = 950, y = 50)

    #label to explain
    info_label = tk.Label(menuFrame, text = "Fill in the information below to find out where the required medicines are available.")
    info_label.pack()

    #label asking for medicine name
    medicine_label = tk.Label(menuFrame, text = "Medicine Name:")
    medicine_label.place(x = 120, y = 110)

    #text box to fill in the name
    global medicine_name
    medicine_name = tk.Entry(menuFrame, justify = "center", width = 35)
    medicine_name.place(x = 250, y = 110)

    #label asking for quantity
    quantity_label = tk.Label(menuFrame, text = "Quantity:")
    quantity_label.place(x = 550, y = 110)

    #text box to fill in the quantity
    global quantity_entry
    quantity_entry = tk.Entry(menuFrame, justify = "center", width = 10)
    quantity_entry.place(x = 650, y = 110)

    #creating buttons for upload and search function
    search_button = tk.Button(menuFrame, activeforeground="blue", text = "Search", command = searchCheck)
    search_button.place(x = 750, y = 105)

    #creating buttons for upload and search function
    upload_button = tk.Button(menuFrame, activeforeground="blue", text = "Upload inventory file", command = upload)
    upload_button.place(x = 850, y = 105)

    menuFrame.mainloop()
    return
