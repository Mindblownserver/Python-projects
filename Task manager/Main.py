import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from ttkthemes import ThemedStyle
import time
import psutil
import subprocess as s
import random

process_pid = []
process_names = []
cpu_percent = []
started_time = []
used_memory = []
nicer_memory = []

# Setting up Main window
win1 = tk.Tk()
style2 = ttk.Style(win1)
style2.configure('Treeview', rowheight=1000)
win1.title("System monitor")
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


def hide_buttone():
    global process_names, process_pid, cpu_percent, started_time, used_memory, nicer_memory
    print("Hidden, to stop the program, press Ctrl+C or Ctrl+Z")
    win1.withdraw()
    load_infos()
    for i in range(len(process_names)):
        if cpu_percent[i] > 50:
            s.Popen(['/usr/bin/aplay', "swiftly.wav"], shell=False)
            s.Popen(['notify-send', "Cpu overusage", "-i", 'face-sad',
                     "Process {} is taking {} of total CPU\n Please close it".format(process_names[i], cpu_percent[i])])
            res = mb.askquestion("CPU overusage", message="Process {} is taking {} of total CPU\n Do you want to close it?".format(process_names[i], cpu_percent[i]))
            if res == "yes":
                Process = psutil.Process(process_pid[i])
                Process.kill()
            else: 
                print("Deletion cancelled")
    time.sleep(5)
    hide_buttone()
    # win1.deiconify()


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


frame_tree = ttk.Frame(win1)
frame_vsb = ttk.Frame(win1)
frame_button = ttk.Frame(win1)

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

load_infos()

for i in range(len(process_pid)):
    tree.insert("", 'end', values=(
        process_pid[i], process_names[i], cpu_percent[i], started_time[i], nicer_memory[i]))


refresh()

tree.bind("<Button-3>", popup)
tree.bind("<Button-1>", gray_in_out)

frame_button.pack(side=tk.BOTTOM, fill=tk.X)
frame_vsb.pack(side=tk.RIGHT, fill=tk.BOTH)
frame_tree.pack(fill=tk.BOTH)
vsb.pack(side=tk.RIGHT, fill=tk.BOTH)
tree.pack(fill=tk.BOTH)
end_button.pack(side=tk.LEFT)
hide_button.pack(side=tk.RIGHT)
win1.mainloop()
