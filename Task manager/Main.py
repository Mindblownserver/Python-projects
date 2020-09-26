#!/usr/bin/env python3
import pkg_resources.py2_warn
import datetime
import os
import random
import subprocess as s
import time
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import psutil
from ttkthemes import ThemedStyle

process_pid = []
process_names = []
cpu_percent = []
started_time = []
used_memory = []
nicer_memory = []
cancelled_processes = []
Profiles = []
path = "Profiles"
Loaded_prof = []
# Setting up Main window
win1 = tk.Tk()
style2 = ttk.Style(win1)
style2.configure('Treeview', rowheight=1000)
win1.title("Pymanager | version: 1.1")
win1.geometry('900x650')
style = ThemedStyle(win1)
style.set_theme('breeze')

# Properties window


def Properties_top():
    top = tk.Toplevel()
    top.title("Properties")
    # Logics
    selected_row = tree.selection()[0]
    Pid = tree.set(selected_row)["1"]
    name = tree.set(selected_row)["2"]
    Cpu = tree.set(selected_row)["3"]
    started = tree.set(selected_row)["4"]
    memory = tree.set(selected_row)["5"]
    # frames
    frame_left = ttk.Frame(top)
    frame_right = ttk.Frame(top)
    # Left
    idd_left = ttk.Label(frame_left, text="Id")
    Name_left = ttk.Label(frame_left, text="Name")
    Cpu_left = ttk.Label(frame_left, text="CPU %")
    Started_left = ttk.Label(frame_left, text="Started at")
    Memory_left = ttk.Label(frame_left, text="Memory used ")
    # Right
    idd_right = ttk.Label(frame_right, text="{}".format(Pid))
    Name_right = ttk.Label(frame_right, text="{}".format(name))
    Cpu_right = ttk.Label(frame_right, text="{}%".format(Cpu))
    Started_right = ttk.Label(frame_right, text="{}".format(started))
    Memory_right = ttk.Label(frame_right, text="{}".format(memory))

    # Packing things up :/
    frame_left.pack(side=tk.LEFT, padx=10)
    frame_right.pack(side=tk.RIGHT, padx=5)
    idd_left.pack(anchor=tk.NW, pady=5)
    Name_left.pack(anchor=tk.NW, pady=5)
    Cpu_left.pack(anchor=tk.NW, pady=5)
    Started_left.pack(anchor=tk.NW, pady=5)
    Memory_left.pack(anchor=tk.NW, pady=5)
    idd_right.pack(anchor=tk.W, pady=5)
    Name_right.pack(anchor=tk.W, pady=5)
    Cpu_right.pack(anchor=tk.W, pady=5)
    Started_right.pack(anchor=tk.W, pady=5)
    Memory_right.pack(anchor=tk.W, pady=5)

# kills process


def kill_function():
    selected_row = tree.selection()[0]
    Pid = tree.set(selected_row)["1"]
    process = psutil.Process(int(Pid))
    print(process.name)
    process.kill()

# kills process


def button_kill():
    selected_row = tree.selection()[0]
    Pid = tree.set(selected_row)["1"]
    process = psutil.Process(int(Pid))
    print(process.name)
    process.kill()

# Gray in and out


def gray_in_out(smthng):
    end_button['state'] = tk.NORMAL

# Hide and ready to push notifications!


x = 0

def hide_buttone():
    global process_names, process_pid, cpu_percent, started_time, used_memory, nicer_memory, Loaded_prof, x
    print("Hidden, to stop the program, press Ctrl+C or Ctrl+Z")
    win1.withdraw()
    load_infos()
    for i in range(len(process_names)):
        if x == 0:
            place = os.getcwd()
            t = s.Popen(['notify-send', "Pymanager",
                         "Hidden, to stop the program, press Ctrl+C or Ctrl+Z", "-i", "{}/index.ico".format(place)])

        try:
            if cpu_percent[i] > 50:
                if process_names[i] not in cancelled_processes:
                    s.Popen(['/usr/bin/aplay', "swiftly.wav"])
                    s.Popen(['notify-send', "Cpu overusage", "-i", 'face-sad',
                             "Process {} is taking {} of total CPU\n Please close it".format(process_names[i], cpu_percent[i])])
                    res = mb.askquestion("CPU overusage", message="Process {} is taking {} of total CPU\n Do you want to close it?".format(
                        process_names[i], cpu_percent[i]))
                    if res == "yes":
                        Process = psutil.Process(process_pid[i])
                        Process.kill()
                    else:
                        print("Added element to list!")
                        cancelled_processes.append(process_names[i])
                        with open("Profiles/{}.ini".format(Loaded_prof[0]), "a+") as file:
                            file.write("\n")
                            file.write("{}".format(process_names[i]))
                else:
                    print("Already cancelled")
        except:
            pass
        x += 1
    time.sleep(5)
    hide_buttone()


    # win1.deiconify()
# Tabs
tab_controle = ttk.Notebook(win1)
tab1 = ttk.Frame(tab_controle)
tab2 = ttk.Frame(tab_controle)
tab_controle.add(tab1, text="Processes")
tab_controle.add(tab2, text="Profile")


# Menu
Menubar = tk.Menu(win1, tearoff=0)
Menubar.add_command(label="Stop")
Menubar.add_command(label="Continue")
Menubar.add_command(label="End", command=kill_function)
Menubar.add_command(label="Kill", command=kill_function)
Menubar.add_separator()
Menubar.add_command(label="Properties", command=Properties_top)

# Adjusting bytes


def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.0f}{unit}B"
        bytes /= 1024

# Loading infos


def load_infos():
    global process_names, process_pid, cpu_percent, started_time, used_memory, nicer_memory

    process_pid.clear()
    process_names.clear()
    cpu_percent.clear()
    started_time.clear()
    used_memory.clear()
    nicer_memory.clear()
    for process in psutil.process_iter():
        with process.oneshot():
            pids = process.pid
            name = process.name()
            started__ = datetime.datetime.fromtimestamp(process.create_time())
            started = started__.strftime("%d/%m/%Y %H:%M:%S")
            cpu_usage = process.cpu_percent()
            try:
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            nicememory = get_size(memory_usage)
            process_pid.append(pids)
            process_names.append(name)
            cpu_percent.append(cpu_usage)
            started_time.append(started)
            used_memory.append(memory_usage)
            nicer_memory.append(nicememory)

# As the name says :|


def refresh():
    # print("ffffffqqsd")
    tree.delete(*tree.get_children())
    end_button['state'] = tk.DISABLED
    load_infos()
    for i in range(len(process_pid)):
        tree.insert("", 'end', values=(
            process_pid[i], process_names[i], cpu_percent[i], started_time[i], nicer_memory[i]))
    tree.after(5000, refresh)

# Right click menu


def popup(event):
    if tree.selection() != ():
        try:
            Menubar.tk_popup(event.x_root + 10, event.y_root)
        finally:
            Menubar.grab_set()
    else:
        pass

# Add profiles


def add_profiles():
    text = cb.get()
    if text not in cb["values"]:
        print("not in list")
        print("Profile "+text+" is successfully added")
        with open("{}/{}.ini".format(path, text), "a+") as file:
            file.write("[Properties]")
            file.write(
                "\n \n Profile_name= {} \n \n [Processes not to notify about]".format(text))
        option = list(cb["values"])
        option.append(text)
        cb["values"] = option
    else:
        print("Already exists")


# Remove profiles


def rmv_profiles():
    text = cb.get()
    items = list(cb["values"])
    items.remove(text)
    cb["values"] = items
    os.remove("{}/{}.ini".format(path, text))
    cb.current(0)

# Load profile


def load_btn():
    global Loaded_prof, cancelled_processes
    cancel = []
    Loaded_prof.clear()
    text = cb.get()
    print("Loading "+text+" profile...")
    lbl = ttk.Label(tab2, text="{} profile is loaded".format(text))
    Loaded_prof.append(text)
    sep.pack(expand=True, fill=tk.X, anchor=tk.N)
    lbl.pack(side=tk.TOP, anchor=tk.N)
    with open("Profiles/{}.ini".format(text), "r") as file:
        reader = file.read()
        red = reader.splitlines()
        for line in red:
            cancel.append(line)
    for i in cancel:
        i.strip(r'\n')
        cancelled_processes.append(i)
    print(cancelled_processes)


# Create profile file


def create_file_load_profiles(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        print("File already exist :)")
    list_dir = os.listdir(path)
    option = list(cb["values"])
    for i in list_dir:
        text = os.path.splitext("{}".format(i))[0]
        if text not in option:
            option.append(text)
        else:
            pass
    cb['values'] = option

# Checking


def check_rmv():
    path = "Profiles"
    list_dir = os.listdir(path)
    if len(list_dir) == 0:
        Delete_btn['state'] = tk.DISABLED
        load_button['state'] = tk.DISABLED
    elif len(list_dir) != 0:
        Delete_btn['state'] = tk.NORMAL
        load_button['state'] = tk.NORMAL
    text = cb.get()
    option = list(cb["values"])
    if cb.get() == "<<Select-profile>>":
        Delete_btn['state'] = tk.DISABLED
        load_button['state'] = tk.DISABLED
    elif text not in option:
        Delete_btn['state'] = tk.DISABLED
        load_button['state'] = tk.DISABLED

    frame_UP.after(250, check_rmv)


# Total composents :) tab 1
frame_tree = ttk.Frame(tab1)
frame_vsb = ttk.Frame(tab1)
frame_button = ttk.Frame(tab1)

vsb = ttk.Scrollbar(frame_vsb, orient="vertical")
tree = ttk.Treeview(frame_tree, height=50, yscrollcommand=vsb.set)
end_button = ttk.Button(frame_button, text="End task",
                        command=button_kill, state=tk.DISABLED)
hide_button = ttk.Button(
    frame_button, text="Hide window", command=hide_buttone)

tree["columns"] = ("1", "2", "3", "4", "5")
tree['show'] = 'headings'
tree.column("1", width=10, anchor='c')
tree.column("2", width=100, anchor="w")
tree.column("3", width=90, anchor='c')
tree.column("4", anchor='c')
tree.column("5", width=173, anchor='w')
tree.heading("1", text="ID")
tree.heading("2", text="Name")
tree.heading("3", text="CPU%")
tree.heading("4", text="Started at")
tree.heading("5", text="Memory")
vsb.config(command=tree.yview)
tree.config(yscrollcommand=vsb.set)

# Total composents of tab 2 :I

frame_UP = ttk.Frame(tab2)
frame_prop = ttk.Frame(tab2)
profile_label = ttk.Label(frame_UP, text="Profile")
cb = ttk.Combobox(frame_UP, width=30)

cb["values"] = ("<<Select-profile>>")

cb.current(0)
Add_btn = ttk.Button(frame_UP, text="Add", command=add_profiles)
Delete_btn = ttk.Button(frame_UP, text="Delete", command=rmv_profiles)
load_button = ttk.Button(frame_UP, text="Load", command=load_btn)
sep = ttk.Separator(tab2, orient=tk.HORIZONTAL)

frame_UP.pack(anchor=tk.NW)
Delete_btn.pack(side=tk.RIGHT, padx=10, pady=10)
load_button.pack(side=tk.RIGHT, padx=10, pady=10)
Add_btn.pack(side=tk.RIGHT, padx=10, pady=10)
cb.pack(side=tk.RIGHT, padx=10, pady=10)

profile_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Actions!

create_file_load_profiles(path)
frame_UP.after(500, check_rmv)
load_infos()

for i in range(len(process_pid)):
    tree.insert("", 'end', values=(
        process_pid[i], process_names[i], cpu_percent[i], started_time[i], nicer_memory[i]))


refresh()

tree.bind("<Button-3>", popup)
tree.bind("<Button-1>", gray_in_out)

tab_controle.pack(expand=1, fill="both")
frame_button.pack(side=tk.BOTTOM, fill=tk.X)
frame_vsb.pack(side=tk.RIGHT, fill=tk.BOTH)
frame_tree.pack(fill=tk.BOTH)
vsb.pack(side=tk.RIGHT, fill=tk.BOTH)
tree.pack(fill=tk.BOTH)
end_button.pack(side=tk.LEFT)

hide_button.pack(side=tk.RIGHT)
win1.mainloop()
