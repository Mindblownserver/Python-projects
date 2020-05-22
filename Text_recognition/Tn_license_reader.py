#!/usr/bin/env python3
import csv
import math
import os
from ttkthemes import ThemedStyle
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import os
import fnmatch
import pytesseract
import cv2
from PIL import ImageTk, Image

lis = []
names =[]
contr =[]
formats = []
img_path = ""
def import_data():
    global lis,names,contr,formats    
    lis.clear()
    names.clear()
    contr.clear()
    formats.clear()
    with open("immat.csv") as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            lis.append(row[0])
            names.append(row[1])
            contr.append(row[2])
            formats.append(row[-1])
def table():
    global tree
    print(lis)
    print(names)
    print(contr)
    print(formats)
    if len(lis) !=0 :
        lis.clear()
        names.clear()
        contr.clear()
        formats.clear()
    import_data()
    
    print(lis)
    print(names)
    print(contr)
    print(formats)
    for i in tree.get_children() :
        tree.delete(i)
    
    for i in range(1,len(lis)):
        tree.insert("", 'end',values=(lis[i], names[i], contr[i], formats[i]) )    
def Img_to_string(filepath):
    #fichier
    base_name = os.path.basename(filepath)
    base_name_pure = os.path.splitext(base_name)
    numbers = ["0","1","2","3","4","5","6","7","8","9"," "]
    list_text_with_char =[]
    img = pytesseract.image_to_string(filepath, lang='ara+eng')
    print(img)
    for char in img:
        list_text_with_char.append(char) 
    text_no_char = [i for i in list_text_with_char if i in numbers]    
    length = len(text_no_char)
    half_index = length //2
    better_halfindex = math.floor(half_index)
    first_half = text_no_char[:better_halfindex]
    second_half = text_no_char[better_halfindex:]
    while (" " in first_half):
        first_half.remove(" ")
    while (" " in second_half):
        second_half.remove(" ") 
    first_half[0 : 3] = ["".join(first_half[0:3])]
    second_half[0 : 4] = ["".join(second_half[0:4])]
    list_to_string1 = ''.join([str(elem) for elem in first_half])
    list_to_string2 = ''.join([str(ele) for ele in second_half])
    with open('immat.csv', 'a+', newline="") as file:
        writer = csv.writer(file, delimiter=',')
        if list_to_string1 =="" or list_to_string2 == "":
            print("Couldn't read image")
            writer.writerow(["Error",base_name_pure[0], "Error", base_name_pure[1]])
        else:    
            writer.writerow([list_to_string1,base_name_pure[0],list_to_string2, base_name_pure[1]])
def open_file():
    file_path = filedialog.askopenfilename(initialdir=img_path, filetypes=[("Picture file format", "*.png"), ("Picture file format", "*.jpg"),("All Files", "*.*")])
    if not file_path:
        return False
    if file_path:
        Img_to_string(file_path)
        table()
def open_directory():
    global img_path
    img_path = tk.filedialog.askdirectory(initialdir='/home/yassine/Pictures/immat')
    if not img_path:
        return
    elif img_path:
        print('Image directory set')
def remove_rows():
    
    selected_row = tree.selection()[0]
    first = tree.set(selected_row)["1"]
    name =tree.set(selected_row)["2"]
    third = tree.set(selected_row)["3"]
    last= tree.set(selected_row)["4"]
    msg_box = tkinter.messagebox.askquestion(message="You are going to remove {},{}, {}, {} from the table".format(first,name, third, last))
    output_data = []
    end_list=[]
    output_data.clear()
    if msg_box == "yes" or msg_box == "Yes" or msg_box == "YES":
        print(selected_row)
        tree.delete(selected_row)
        for child in tree.get_children():
                print('success')
                output_data.append(tree.item(child)["values"])    
    else:
        print('Cancel deletion')    
    print(output_data)
    with open("immat.csv", "w",newline="") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["Serie", "Nom", "Matricule", "Format"])
        list2d_to_lists(output_data, end_list)
        print(end_list)
        for i in range(len(output_data)):
            writer.writerow((end_list[i], end_list[i+1], end_list[i+2], end_list[i+3]))
def list2d_to_lists(output_dat, otherlist):
    for sublist in output_dat:
        for item in sublist:
            otherlist.append(item)
def top_lvl_help ():
    Top = tk.Toplevel(win1)
    Top.geometry("400x250")
    Top.resizable(False, False)
    Top.title('Troubleshoot')
    
    def yes11():
        tk.messagebox.showinfo(message='Then the Image is not clear..\n Make sure the content(numbers) is big not small')
    def yes22():
        tk.messagebox.showinfo(message='Decrease the quality of the image')
    def git():
        top = tk.Tk()
        top.resizable(False, False)
        top.geometry("500x100")
        top.title('Publish issue at github')
        entryy = ttk.Entry(top)
        entryy.insert(0,"https://github.com/Mindblownserver/Python-projects")
        entryy.config(state='readonly')
        entryy.pack(fill= tk.X)
        top.mainloop()
    prb1 = ttk.Label(master=Top, text="Displaying Error Error text")
    yes1_button = ttk.Button(master=Top, text= "Yes", command=yes11)
    prb2 = ttk.Label(master=Top, text="Displaying wrong numbers")
    yes2_button = ttk.Button(master=Top, text='Yes', command=yes22)
    prb3 = ttk.Label(master=Top, text='Unmentioned problem :(')
    yes3 = ttk.Button(master=Top, text="Yes :(", command=git)
    
    prb1.pack(pady=8)
    yes1_button.pack(fill= tk.X, pady=8)
    prb2.pack()
    yes2_button.pack(fill= tk.X,pady=8)
    prb3.pack(pady=8)
    yes3.pack(fill= tk.X, pady=8)
    Top.mainloop()

win1 =tk.Tk()
win1.resizable(False, False)
style2 = ttk.Style(win1)
style2.configure('Treeview', rowheight=1000)
win1.title("Immatriculation des voitures en Tunisie")
win1.geometry('1330x720')
style = ThemedStyle(win1)
style.set_theme('breeze')
Menubar = tk.Menu(win1)
win1.config(menu=Menubar)
submenu = tk.Menu(Menubar, tearoff=0)
submenu1 = tk.Menu(Menubar, tearoff=0)
submenu2 = tk.Menu(master= Menubar, tearoff=0)
Menubar.add_cascade(label="File", menu=submenu)
Menubar.add_cascade(label="Edit", menu=submenu1)
Menubar.add_cascade(label= "Help", menu=submenu2)
submenu2.add_command(label='Troubleshoot', command=top_lvl_help)
submenu1.add_command(label="Remove row", command=remove_rows)
submenu.add_command(label="Set image directory", command=open_directory)
submenu.add_command(label="Import", command=open_file)
submenu.add_command(label="Exit", command=win1.quit)


def search_for_file (filename, path, results):
    results.clear()
    for root ,dirs, files in os.walk(path):
        if filename in files:
            results.append(os.path.join(root, filename))
def row_to_picturee(event):
    global img_path
    try:
        result =[]
        identification = tree.identify_row(event.y)
        name = tree.set(identification)["2"]
        name_ext = name + tree.set(identification)["4"]
        
        search_for_file(name_ext, img_path, result)    
        print(result)
        photo = Image.open(result[0])
        new_photo = photo.resize((390, 77))
        img = ImageTk.PhotoImage(new_photo)
            
        image_lbl['image'] = img
        image_lbl.image = img
    except KeyError:
        print('')
#create tree
frm_pic = ttk.Frame(win1)
image_lbl = ttk.Label(frm_pic, image="")
vsb = ttk.Scrollbar(win1, orient="vertical")
tree = ttk.Treeview(win1, height=32, yscrollcommand=vsb.set )
tree["columns"] = ("1", "2", "3", "4")
tree['show'] = 'headings' 
tree.column("1", width = 173,anchor ='c') 
tree.column("2", width = 173, anchor ="c") 
tree.column("3", width = 173,anchor ='c') 
tree.column("4", width = 173,anchor ='c')
tree.heading("1", text ="Serie") 
tree.heading("2", text ="Nom") 
tree.heading("3", text ="Matricule") 
tree.heading("4", text ="Format")
tree.bind("<ButtonRelease-1>",row_to_picturee)
vsb.config(command=tree.yview)
vsb.pack(side=tk.LEFT, fill='y')
tree.pack(side=tk.LEFT)
tk.messagebox.showinfo(title="Info", message='Make sure to read text file before using the app :)')
tk.messagebox.showinfo(title="Info", message="Make sure to you don't have two files with same name :)")
frm_pic.pack(side=tk.TOP)
image_lbl.pack()    

win1.mainloop()
