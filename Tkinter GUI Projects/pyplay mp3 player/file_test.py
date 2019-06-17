import tkinter

#tkinter._test()

import tkinter as tk

window = tk.Tk() #tk.Tk() return a widget which is window


pic = tk.PhotoImage(file="lover.gif")
button = tk.Button(window, text='Stop', width=10, command=window.destroy, bg="red", fg="white", font="Consolas 12 italic")

label = tk.Label(window, text="Hello Tkinter!", image=pic, compound = tk.CENTER, padx = 10 \
                 , fg="red", font="Verdana 10 bold") #creating a label on the window


label.pack(side="right") #put the label on the window
button.pack(side="right") #put the button on the window

window.mainloop() #loop through the window