#!/usr/bin/env python3

# Importing some stuff
import fbchat
from fbchat import Client
from ttkthemes import ThemedStyle

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    from Tkinter import ttk
import requests
import os
from io import BytesIO
from PIL import ImageTk, Image
import time

user_id = 0
colours = [
    "snow",
    "ghost white",
    "white smoke",
    "gainsboro",
    "floral white",
    "old lace",
    "linen",
    "antique white",
    "papaya whip",
    "blanched almond",
    "bisque",
    "peach puff",
    "navajo white",
    "lemon chiffon",
    "mint cream",
    "azure",
    "alice blue",
    "lavender",
    "lavender blush",
    "misty rose",
    "dark slate gray",
    "dim gray",
    "slate gray",
    "light slate gray",
    "gray",
    "light grey",
    "midnight blue",
    "navy",
    "cornflower blue",
    "dark slate blue",
    "slate blue",
    "medium slate blue",
    "light slate blue",
    "medium blue",
    "royal blue",
    "blue",
    "dodger blue",
    "deep sky blue",
    "sky blue",
    "light sky blue",
    "steel blue",
    "light steel blue",
    "light blue",
    "powder blue",
    "pale turquoise",
    "dark turquoise",
    "medium turquoise",
    "turquoise",
    "cyan",
    "light cyan",
    "cadet blue",
    "medium aquamarine",
    "aquamarine",
    "dark green",
    "dark olive green",
    "dark sea green",
    "sea green",
    "medium sea green",
    "light sea green",
    "pale green",
    "spring green",
    "lawn green",
    "medium spring green",
    "green yellow",
    "lime green",
    "yellow green",
    "forest green",
    "olive drab",
    "dark khaki",
    "khaki",
    "pale goldenrod",
    "light goldenrod yellow",
    "light yellow",
    "yellow",
    "gold",
    "light goldenrod",
    "goldenrod",
    "dark goldenrod",
    "rosy brown",
    "indian red",
    "saddle brown",
    "sandy brown",
    "dark salmon",
    "salmon",
    "light salmon",
    "orange",
    "dark orange",
    "coral",
    "light coral",
    "tomato",
    "orange red",
    "red",
    "hot pink",
    "deep pink",
    "pink",
    "light pink",
    "pale violet red",
    "maroon",
    "medium violet red",
    "violet red",
    "medium orchid",
    "dark orchid",
    "dark violet",
    "blue violet",
    "purple",
    "medium purple",
    "thistle",
    "snow2",
    "snow3",
    "snow4",
    "seashell2",
    "seashell3",
    "seashell4",
    "AntiqueWhite1",
    "AntiqueWhite2",
    "AntiqueWhite3",
    "AntiqueWhite4",
    "bisque2",
    "bisque3",
    "bisque4",
    "PeachPuff2",
    "PeachPuff3",
    "PeachPuff4",
    "NavajoWhite2",
    "NavajoWhite3",
    "NavajoWhite4",
    "LemonChiffon2",
    "LemonChiffon3",
    "LemonChiffon4",
    "cornsilk2",
    "cornsilk3",
    "cornsilk4",
    "ivory2",
    "ivory3",
    "ivory4",
    "honeydew2",
    "honeydew3",
    "honeydew4",
    "LavenderBlush2",
    "LavenderBlush3",
    "LavenderBlush4",
    "MistyRose2",
    "MistyRose3",
    "MistyRose4",
    "azure2",
    "azure3",
    "azure4",
    "SlateBlue1",
    "SlateBlue2",
    "SlateBlue3",
    "SlateBlue4",
    "RoyalBlue1",
    "RoyalBlue2",
    "RoyalBlue3",
    "RoyalBlue4",
    "blue2",
    "blue4",
    "DodgerBlue2",
    "DodgerBlue3",
    "DodgerBlue4",
    "SteelBlue1",
    "SteelBlue2",
    "SteelBlue3",
    "SteelBlue4",
    "DeepSkyBlue2",
    "DeepSkyBlue3",
    "DeepSkyBlue4",
    "SkyBlue1",
    "SkyBlue2",
    "SkyBlue3",
    "SkyBlue4",
    "LightSkyBlue1",
    "LightSkyBlue2",
    "LightSkyBlue3",
    "LightSkyBlue4",
    "SlateGray1",
    "SlateGray2",
    "SlateGray3",
    "SlateGray4",
    "LightSteelBlue1",
    "LightSteelBlue2",
    "LightSteelBlue3",
    "LightSteelBlue4",
    "LightBlue1",
    "LightBlue2",
    "LightBlue3",
    "LightBlue4",
    "LightCyan2",
    "LightCyan3",
    "LightCyan4",
    "PaleTurquoise1",
    "PaleTurquoise2",
    "PaleTurquoise3",
    "PaleTurquoise4",
    "CadetBlue1",
    "CadetBlue2",
    "CadetBlue3",
    "CadetBlue4",
    "turquoise1",
    "turquoise2",
    "turquoise3",
    "turquoise4",
    "cyan2",
    "cyan3",
    "cyan4",
    "DarkSlateGray1",
    "DarkSlateGray2",
    "DarkSlateGray3",
    "DarkSlateGray4",
    "aquamarine2",
    "aquamarine4",
    "DarkSeaGreen1",
    "DarkSeaGreen2",
    "DarkSeaGreen3",
    "DarkSeaGreen4",
    "SeaGreen1",
    "SeaGreen2",
    "SeaGreen3",
    "PaleGreen1",
    "PaleGreen2",
    "PaleGreen3",
    "PaleGreen4",
    "SpringGreen2",
    "SpringGreen3",
    "SpringGreen4",
    "green2",
    "green3",
    "green4",
    "chartreuse2",
    "chartreuse3",
    "chartreuse4",
    "OliveDrab1",
    "OliveDrab2",
    "OliveDrab4",
    "DarkOliveGreen1",
    "DarkOliveGreen2",
    "DarkOliveGreen3",
    "DarkOliveGreen4",
    "khaki1",
    "khaki2",
    "khaki3",
    "khaki4",
    "LightGoldenrod1",
    "LightGoldenrod2",
    "LightGoldenrod3",
    "LightGoldenrod4",
    "LightYellow2",
    "LightYellow3",
    "LightYellow4",
    "yellow2",
    "yellow3",
    "yellow4",
    "gold2",
    "gold3",
    "gold4",
    "goldenrod1",
    "goldenrod2",
    "goldenrod3",
    "goldenrod4",
    "DarkGoldenrod1",
    "DarkGoldenrod2",
    "DarkGoldenrod3",
    "DarkGoldenrod4",
    "RosyBrown1",
    "RosyBrown2",
    "RosyBrown3",
    "RosyBrown4",
    "IndianRed1",
    "IndianRed2",
    "IndianRed3",
    "IndianRed4",
    "sienna1",
    "sienna2",
    "sienna3",
    "sienna4",
    "burlywood1",
    "burlywood2",
    "burlywood3",
    "burlywood4",
    "wheat1",
    "wheat2",
    "wheat3",
    "wheat4",
    "tan1",
    "tan2",
    "tan4",
    "chocolate1",
    "chocolate2",
    "chocolate3",
    "firebrick1",
    "firebrick2",
    "firebrick3",
    "firebrick4",
    "brown1",
    "brown2",
    "brown3",
    "brown4",
    "salmon1",
    "salmon2",
    "salmon3",
    "salmon4",
    "LightSalmon2",
    "LightSalmon3",
    "LightSalmon4",
    "orange2",
    "orange3",
    "orange4",
    "DarkOrange1",
    "DarkOrange2",
    "DarkOrange3",
    "DarkOrange4",
    "coral1",
    "coral2",
    "coral3",
    "coral4",
    "tomato2",
    "tomato3",
    "tomato4",
    "OrangeRed2",
    "OrangeRed3",
    "OrangeRed4",
    "red2",
    "red3",
    "red4",
    "DeepPink2",
    "DeepPink3",
    "DeepPink4",
    "HotPink1",
    "HotPink2",
    "HotPink3",
    "HotPink4",
    "pink1",
    "pink2",
    "pink3",
    "pink4",
    "LightPink1",
    "LightPink2",
    "LightPink3",
    "LightPink4",
    "PaleVioletRed1",
    "PaleVioletRed2",
    "PaleVioletRed3",
    "PaleVioletRed4",
    "maroon1",
    "maroon2",
    "maroon3",
    "maroon4",
    "VioletRed1",
    "VioletRed2",
    "VioletRed3",
    "VioletRed4",
    "magenta2",
    "magenta3",
    "magenta4",
    "orchid1",
    "orchid2",
    "orchid3",
    "orchid4",
    "plum1",
    "plum2",
    "plum3",
    "plum4",
    "MediumOrchid1",
    "MediumOrchid2",
    "MediumOrchid3",
    "MediumOrchid4",
    "DarkOrchid1",
    "DarkOrchid2",
    "DarkOrchid3",
    "DarkOrchid4",
    "purple1",
    "purple2",
    "purple3",
    "purple4",
    "MediumPurple1",
    "MediumPurple2",
    "MediumPurple3",
    "MediumPurple4",
    "thistle1",
    "thistle2",
    "thistle3",
    "thistle4",
    "gray1",
    "gray2",
    "gray3",
    "gray4",
    "gray5",
    "gray6",
    "gray7",
    "gray8",
    "gray9",
    "gray10",
    "gray11",
    "gray12",
    "gray13",
    "gray14",
    "gray15",
    "gray16",
    "gray17",
    "gray18",
    "gray19",
    "gray20",
    "gray21",
    "gray22",
    "gray23",
    "gray24",
    "gray25",
    "gray26",
    "gray27",
    "gray28",
    "gray29",
    "gray30",
    "gray31",
    "gray32",
    "gray33",
    "gray34",
    "gray35",
    "gray36",
    "gray37",
    "gray38",
    "gray39",
    "gray40",
    "gray42",
    "gray43",
    "gray44",
    "gray45",
    "gray46",
    "gray47",
    "gray48",
    "gray49",
    "gray50",
    "gray51",
    "gray52",
    "gray53",
    "gray54",
    "gray55",
    "gray56",
    "gray57",
    "gray58",
    "gray59",
    "gray60",
    "gray61",
    "gray62",
    "gray63",
    "gray64",
    "gray65",
    "gray66",
    "gray67",
    "gray68",
    "gray69",
    "gray70",
    "gray71",
    "gray72",
    "gray73",
    "gray74",
    "gray75",
    "gray76",
    "gray77",
    "gray78",
    "gray79",
    "gray80",
    "gray81",
    "gray82",
    "gray83",
    "gray84",
    "gray85",
    "gray86",
    "gray87",
    "gray88",
    "gray89",
    "gray90",
    "gray91",
    "gray92",
    "gray93",
    "gray94",
    "gray95",
    "gray97",
    "gray98",
    "gray99",
]
# Taking your account information
wn = tk.Tk()
wn.title('Information')
name = ''
password = ''
def submit():
    global name, password
    name = name_entry.get()
    password = pass_entry.get()
    wn.after(500, wn.destroy)

name_entry=ttk.Entry(wn)
pass_entry = ttk.Entry(wn)
sumbit_btn = ttk.Button(wn, text='confirm', command=submit)
name_entry.pack()
pass_entry.pack()
sumbit_btn.pack(side=tk.BOTTOM)
name_entry.insert(3, "Facebook username")
pass_entry.insert(3, 'Facebook password')
wn.mainloop()
client = fbchat.Client(name, password)
users = client.fetchAllUsers()
print(len([user.name for user in users]))

# Making the window
win = tk.Tk()
win.title(name)
style = ThemedStyle(win)
style.set_theme('breeze')
win.geometry("750x670")
win.resizable(False, False)

# Doing colors , you can't really be sent coloured though :(
def open_top_levl_colours():
    Top = tk.Toplevel(win)
    Top.geometry("300x400")
    Top.resizable(False, False)
    color = ""

    def validate():
        global color
        color = colours_cmbox.get()
        print(color)
        entry_text["fg"] = color
        Top.destroy()

    validate_btn = ttk.Button(Top, text="Validate", command=validate)
    colour = tk.StringVar()
    colours_cmbox = ttk.Combobox(Top, width=30, textvariable=colour)
    colours_cmbox["values"] = [i for i in colours]

    validate_btn.pack()
    colours_cmbox.current()
    colours_cmbox.pack()
    Top.mainloop


times = 1

# Doing send all function
def open_top_level_send():
    Top = tk.Toplevel(win)
    Top.geometry("300x400")
    Top.resizable(False, False)
    ch = tk.BooleanVar()
    global times

    def validate():
        global times
        if ch.get() == 1:
            print("Checked")
            for i in [user.uid for user in users]:
                client.send(fbchat.models.Message(entry_message.get()), i)
                time.sleep(0.13 * times)
                times += 0.2    

        elif ch.get() == 0:
            print("Unchecked")
            print("nothing to send.. :(")
        Top.destroy()

    # Check button..etc GUI
    validate_btn = ttk.Button(Top, text="Validate", command=validate)
    check_frnds = ttk.Checkbutton(
        Top, text="Send to all your friends", variable=ch, onvalue=1, offvalue=0
    )
    entry_message = ttk.Entry(Top, width=50)
    check_frnds.pack()
    entry_message.pack()
    validate_btn.pack()
    Top.mainloop


# about app GUI
def open_top_level_about():
    Top = tk.Toplevel(win)
    Top.geometry("450x400")
    Top.resizable(False, False)
    Top.title("about..")
    label = tk.Label(
        Top,
        text="""This app was created by Mohammed Yassine Kharrat 
        in python using Tkinter module as GUI and fbchat as api""",
        fg="pale violet red",
    )
    label.pack()
    Top.mainloop


# Preparing Menu
Menubar = tk.Menu(win)
win.config(menu=Menubar)
submenu = tk.Menu(Menubar, tearoff=0)
submenu2 = tk.Menu(Menubar, tearoff=0)
submenu3 = tk.Menu(Menubar, tearoff=0)
Menubar.add_cascade(label="account", menu=submenu)
Menubar.add_cascade(label="Text", menu=submenu2)
Menubar.add_cascade(label="About", menu=submenu3)
submenu3.add_command(label="about app", command=open_top_level_about)
submenu2.add_command(label="Change colour", command=open_top_levl_colours)
submenu2.add_command(label="send message to all", command=open_top_level_send)
submenu.add_command(label="logout", command=win.quit)
# Taking photo from path
photo = tk.PhotoImage(file="/home/yassine/Desktop/python/samples/PNG/Send.png")
name = ""
identification = 0

# Check the friend function
def check_cmbo(event):
    global name, identification
    friende = frnds_cb.get()
    index1 = [user.name for user in users].index(friende)
    print(index1)
    identification = [user.uid for user in users][index1]
    print(identification)
    # check for profile pic
    print([user.photo for user in users][index1])
    img_url = [user.photo for user in users][index1]
    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    frnd_img["image"] = img
    frnd_img.image = img


# send message function
def send_message():

    text = entry_text.get()
    print(text)
    client.send(fbchat.models.Message(text), identification)
    entry_text.delete(0, tk.END)


# Doing other important GUI
frame_down = tk.Frame(win)
frame_frnds = tk.Frame(win)
lbl = ttk.Label(win, text="Welcome!!")
entry_text = ttk.Entry(frame_down, width=50)
text_bfr_entry = ttk.Label(frame_down, text="Text")
send_butn = ttk.Button(frame_down, command=send_message)
frnd_img = ttk.Button(frame_frnds, image="")
Label_warning = ttk.Label(
    win,
    text="""This can get your account temporarily blocked for spam! 
    (You should execute the script at max about 10 times a day)""",
    
)

num = tk.StringVar()
lbl_frnds = ttk.Label(frame_frnds, text="Friends")
frnds_cb = ttk.Combobox(frame_frnds, width=20, textvariable=num)
# Adding friends' to the list
frnds_cb["values"] = [user.name for user in users]
frnds_cb.current()
frnds_cb.bind("<<ComboboxSelected>>", check_cmbo)
# Packing or displaying them

lbl.pack()
Label_warning.pack()
frame_frnds.pack(side=tk.BOTTOM)
frame_down.pack(side=tk.BOTTOM)
text_bfr_entry.pack(side=tk.LEFT)
frnds_cb.pack(side=tk.LEFT)
lbl_frnds.pack(side=tk.RIGHT)
entry_text.pack(side=tk.LEFT)
frnd_img.pack(side=tk.RIGHT)
send_butn.pack()
win.mainloop()
