#!/usr/bin/env python3

from tkinter import *
from numpy import *
from itertools import *
import tempfile
import time
import pandas
import csv
import subprocess

## Create if statment to look for stockusage.txt and create it if not found


colnames = ['date', 'name', 'stock']
data = pandas.read_csv('stuff/stockusage.txt')#, names = colnames)

date = list(data.date)
name = list(data.name)
stock = list(data.stock)

class Window(Frame):
    
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
    
    # Creation of init_window
    def init_window(self):
        
        # Title of our master widget
        self.master.title('Stock counter')
        
        # Allowing the widget to take the full space of the root window
        self.pack(fill = BOTH, expand = 1)
        
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # add commands to the menu
        file.add_command(label = 'Graph', command = self.graph_data)
        file.add_command(label="Exit", command = self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu = file)

        # Entry for stock number
        stockLabel = Label(self, text = 'Stock number taken:')
        stockLabel.place(x = 5, y = 25)        
        self.stockEntry = Entry(self)
        self.stockEntry.place(x = 130, y = 25)
        
        # Entry for name
        nameLabel = Label(self, text = 'Name:')
        nameLabel.place(x = 5, y = 50)
        self.nameEntry = Entry(self)
        self.nameEntry.place(x = 130, y = 50)
        
        # Create and position Enter button
        
        enterButton = Button(self, text = 'Enter', command = self.get_values)
        enterButton.place(x = 150, y = 85)
        
        # Create and position quitButton
        quitButton = Button(self, text = 'Quit', command  = self.client_exit)
        quitButton.place(x = 213, y = 85)

    def client_exit(self):
        root.destroy()

    def get_values(self):
        date.append(time.strftime("%d-%m-%Y"))
        name.append(self.nameEntry.get())
        stock.append(int(self.stockEntry.get()))
        # Clears entry of text
        self.stockEntry.delete(0, 'end')
        self.nameEntry.delete(0, 'end')
        self.write_data()
        
    def write_data(self):
        returnValues = (date, name, stock)
        with open("stuff/stockusage.txt","w+") as f:
            writer = csv.writer(f)
            writer.writerow(colnames)
            for values in zip_longest(*returnValues):
                writer.writerow(values)
    
    def graph_data(self):
        returnValues = (date, name, stock)
        # Create temp file for graphdata to be written to
        tmp = tempfile.mkstemp(suffix=".txt", text=True)[1]
        sep = '\t'
        with open(tmp, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(colnames)
            for values in zip_longest(*returnValues):
                writer.writerow(values)
        # Execute R script and send tmp graphdata file        
        proc = subprocess.Popen(['stuff/graphstocks.R', tmp], stdout=subprocess.PIPE)
        #se = proc.communicate()        
        #print(se)
   

root = Tk()

# Size of window
root.geometry('300x125')

app = Window(root)

root.mainloop()