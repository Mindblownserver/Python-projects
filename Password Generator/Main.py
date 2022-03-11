from random import choice
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedStyle
# Adjusting window settigns
window = tk.Tk()
window.configure(bg ="#3c3d95")
window.title("Password Generator")
#window.resizable(False,False)
style = ThemedStyle()
style.set_theme("breeze")
window.geometry("700x500")
# Creating widgets
Symboles = ["}","{","+","_",")","(","^","$","!","@",",",")",">","?","#","/","*","-"]
purpleFrame_bg = "#242459"
purple_widg_bg = "#151636"
wh_text = "white"
pad_x= 10
pad_y = 20

frm = tk.Frame(window, background= purpleFrame_bg)
frm2 = tk.Frame(frm, background= purpleFrame_bg)
title = tk.Label(frm, text="Password Generator",fg=wh_text ,bg= purpleFrame_bg ,font=("Nueva Std Cond", "16"))
entr_pass = tk.Entry(frm,width=60, fg=wh_text ,bg=purple_widg_bg, borderwidth=2)
pass_length = tk.Label(frm2,text="Password length", fg=wh_text ,bg= purpleFrame_bg ,font=("Nueva Std Cond", "10"))
max_length_entr = tk.Entry(frm2,width=10, text="16")
gen_btn = tk.Button(frm, width=52, text="Generate password",relief=tk.FLAT ,fg=wh_text, bg= purple_widg_bg)


entr_pass.insert(0,"Type the base of password")
# functions

def generate(event, lim):
    ch = entr_pass.get().upper()
    entr_pass.delete(0, tk.END)
    passw = ""
    n=1
    for i in range(len(ch)):
        if i == len(ch)//2:
            passw += ch[len(ch)//2]
        elif ch[i] in ["A","E","I","O","U","Y"]:
            passw = passw + str(ord(ch[i]))
            n+=1
        else:
            passw += ch[i] 
    passw += n*"*"
    try:
        while len(passw) < int(lim):
            passw += choice(Symboles)
    except:
        messagebox.showerror("Invalid number", "You either have typed an invalid number in the maximum length box or left it empty")
        passw = ""
    entr_pass.insert(0, passw)
    

gen_btn.bind("<Button-1>", lambda x: generate(x,max_length_entr.get()))
# packing widgets
frm.pack(pady=100)
title.pack(pady=pad_y)
entr_pass.pack(padx= pad_x)
frm2.pack(fill=tk.X)
pass_length.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
max_length_entr.pack(side= tk.RIGHT, padx= pad_x, pady=pad_y)
gen_btn.pack(pady=pad_y, padx= pad_x)
window.mainloop()
