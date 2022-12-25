from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('500x400')

menubar = Menu(root)
root.configure(menu=menubar)

file = Menu(menubar, tearoff=False)
menubar.add_cascade(label='File', menu=file)

file.add_command(label='Open...')
file.add_command(label='Open Folder...')

submenu = Menu(file)
file.add_cascade(label='Submenu', menu=submenu)

file.add_command(label='Exit', command=root.quit)


root.mainloop()