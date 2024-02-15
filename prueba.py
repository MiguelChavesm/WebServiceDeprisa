from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
root = Tk()
stl = ttk.Style()
stl.map('C.TButton',
     foreground = [('pressed','red'),('active','blue')],
     background = [('pressed','!disabled','black'),('active','white')]
)
#background not changing.It is still grey
ttk.Button(root, text='This is a button', style='C.TButton').pack()
root.mainloop()