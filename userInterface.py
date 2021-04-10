from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import mdpandquadtree


def changeValueSRow():
    value = maximumRow.get()
    if(value !='Please select value'):
        maximumR = int(maximumRow.get())
        print(maximumR)
        num = list(range(2,maximumR-1))
        num.insert(0,'Please select value')
        startingRow['values'] = list(num)

def changeValueSCol():
    value = maximumColumn.get()
    if(value !='Please select value'):
        maximumC = int(maximumColumn.get())
        print(maximumC)
        num = list(range(2,maximumC-1))
        num.insert(0,'Please select value')
        startingColumn['values'] = list(num)

def changeValueERow():
    value = maximumRow.get()
    if(value !='Please select value'):
        endingR = int(maximumRow.get())
        print(endingR)
        num = list(range(2,endingR-1))
        num.insert(0,'Please select value')
        endingRow['values'] = list(num)

def changeValueECol():
    value = maximumColumn.get()
    if(value !='Please select value'):
        endingC = int(maximumColumn.get())
        print(endingC)
        num = list(range(2,endingC-1))
        num.insert(0,'Please select value')
        endingColumn['values'] = list(num)

def changeNumberofObstacles():
    mR = maximumRow.get()
    mC = maximumColumn.get()
    if(mR!='Please select value' and mC!='Please select value'):
        mR = int(mR)-1
        mC = int(mC)-1
        num = list(range(1,int((mR*mC)/2)-3))
        num.insert(0,'Please select value')
        numberObstacles['values'] = tuple(num)
    
    
# Creating tkinter window
window = tk.Tk()
window.title('Roboust Motion Planning')
window.geometry('750x375')
# label text for title
ttk.Label(window, text = "Roboust Motion Planning",
		background = 'green', foreground ="white",
		font = ("Times New Roman", 25)).grid(row = 0,column=0,columnspan=7)

# label and Combox for Maximum Row
ttk.Label(window, text = "Select the Maximum Row :",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 5, padx = 10, pady = 25)

maximumRow = tk.StringVar()
maximumRow = ttk.Combobox(window, width = 27, textvariable = maximumRow,state="readonly")
num = list(range(4,16))
num.insert(0,'Please select value')
maximumRow['values'] = list(num)
maximumRow.current(0)
maximumRow.grid(column=1,row=5)
maximumRow.current()

# label and Combox for Maximum Column
ttk.Label(window, text = "Select the Maximum Column :",
		font = ("Times New Roman", 10)).grid(column = 2,
		row = 5, padx = 10, pady = 25)
maximumColumn = tk.StringVar()
maximumColumn = ttk.Combobox(window, width = 27, textvariable = maximumColumn,state="readonly")
num = list(range(4,16))
num.insert(0,'Please select value')
maximumColumn['values'] = list(num)
maximumColumn.current(0)
maximumColumn.grid(column=3,row=5)
maximumColumn.current()


# label and Combox for Starting Row
ttk.Label(window, text = "Select the Starting Row :",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 6, padx = 10, pady = 25)

startingRow = tk.StringVar()
startingRow = ttk.Combobox(window, width = 27, textvariable = startingRow,state="readonly",postcommand= changeValueSRow)
num = []
num.insert(0,'Please select value')
startingRow['values'] = list(num)
startingRow.current(0)
startingRow.grid(column=1,row=6)
startingRow.current()

# label and Combox for Starting Column
ttk.Label(window, text = "Select the Starting Column :",
		font = ("Times New Roman", 10)).grid(column = 2,
		row = 6, padx = 10, pady = 25)

startingColumn = tk.StringVar()
startingColumn = ttk.Combobox(window, width = 27, textvariable = startingColumn,state="readonly",postcommand= changeValueSCol)
num = []
num.insert(0,'Please select value')
startingColumn['values'] = list(num)
startingColumn.current(0)
startingColumn.grid(column=3,row=6)
startingColumn.current()

# label and Combox for Ending Row
ttk.Label(window, text = "Select the Ending Row :",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 7, padx = 10, pady = 25)

endingRow = tk.StringVar()
endingRow = ttk.Combobox(window, width = 27, textvariable = endingRow,state="readonly",postcommand=changeValueERow)
num = []
num.insert(0,'Please select value')
endingRow['values'] = tuple(num)
endingRow.current(0)
endingRow.grid(column=1,row=7)
endingRow.current()

# label and Combox for Ending Column
ttk.Label(window, text = "Select the Ending Column :",
		font = ("Times New Roman", 10)).grid(column = 2,
		row = 7, padx = 10, pady = 25)

endingColumn = tk.StringVar()
endingColumn = ttk.Combobox(window, width = 27, textvariable = endingColumn,state="readonly",postcommand=changeValueECol)
num = []
num.insert(0,'Please select value')
endingColumn['values'] = tuple(num)
endingColumn.current(0)
endingColumn.grid(column=3,row=7)
endingColumn.current()

# label and Combox for number of obstacles
ttk.Label(window, text = "Select the Number of Obstacles :",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 8, padx = 10, pady = 25,columnspan=3)

numberObstacles = tk.StringVar()
numberObstacles = ttk.Combobox(window, width = 27, textvariable = numberObstacles,state="readonly",postcommand=changeNumberofObstacles)
num = []
num.insert(0,'Please select value')
numberObstacles['values'] = tuple(num)
numberObstacles.current(0)
numberObstacles.grid(column=2,row=8,columnspan=2)
numberObstacles.current()

values={}
def validation():
    startRow = startingRow.get()
    startCol = startingColumn.get()
    goalRow = endingRow.get()
    goalCol = endingColumn.get()
    num_obstacle_pts = numberObstacles.get()
    maxRow = maximumRow.get()
    maxCol = maximumColumn.get()
    flag= False
    #validation for maximum row
    if(maxRow == 'Please select value'):
        flag = True
        mb.showinfo("Maximum Row Error","Please select valid maximum row")
        return
    else:
        values['maxRow'] = int(maxRow)

    #validation for maximum col
    if(maxCol == 'Please select value'):
        flag = True
        mb.showinfo("Maximum Column Error","Please select valid maximum column")
        return
    else:
        values['maxCol'] = int(maxCol)
            
    #validation for starting row    
    if(startRow == 'Please select value'):
        flag = True
        mb.showinfo("Starting Row Error", "Please select valid starting row")
        return
    else:
        values['startRow'] = int(startRow)

    #validation for starting col
    if(startCol == 'Please select value'):
        flag = True
        mb.showinfo("Starting Column Error", "Please select valid starting column")
        return
    else:
        values['startCol'] = int(startCol)

    #validation for ending row
    if(goalRow == 'Please select value'):
        flag = True
        mb.showinfo("Ending Row Error", "Please select valid ending row")
        return
    else:
        values['goalRow'] = int(goalRow)

    #validation for ending col
    if(goalCol == 'Please select value'):
        flag = True
        mb.showinfo("Ending Column Error", "Please select valid ending column")
        return
    else:
        values['goalCol'] = int(goalCol)

    #validation for number of obstacles
    if(num_obstacle_pts == 'Please select value'):
        flag = True
        mb.showinfo("Obstacles Error", "Please select valid number of obstacles")
        return
    else:
        values['num_obstacle_pts'] = int(num_obstacle_pts)
    startRow = int(startRow)
    startCol = int(startCol)
    goalRow = int(goalRow)
    goalCol = int(goalCol)
    
    if((startRow,startCol)==(goalRow,goalCol)):
        flag=True
        mb.showinfo("Point Error","Starting Point and ending Point Same. Please enter valid points")
        return
    if(flag==False):
        print(values)
        window.destroy()
        mdpandquadtree.mainfuction(values)
        
        
  
        
B = tk.Button(window,text ="Start Roboust Motion Planning", command = validation,bg='#89cfef').grid(row=9,column=0,columnspan=7)

window.resizable(False, False)
window.mainloop()
