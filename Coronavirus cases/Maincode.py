"""
@Creator : Yassing Kharrat
"""
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import time
import random
from io import BytesIO
from PIL import ImageTk, Image
import tkinter.font as tkfont

all_url = []
flags_url_all = []
additional_name = []
no_add_sp_char = []
name_countries = []
names = []
country_names = []
total_infos = []
Confirmed_cases = []
cases_1M = []
Recovered_cases = []
death_cases = []
url_all = "https://news.google.com/covid19/map?hl=en-US&gl=US&ceid=US%3Aen"
url = "https://news.google.com/covid19/map?hl=en-US&gl=US&ceid=US%3Aen&mid=%2Fm%2F"
text_lbl_list = [
    "Sending request",
    "waiting for response",
    "Fetching informations",
    "Translating bytes to images",
    "Translating binaries to words",
]


# get_url(url)
# infos_to_lists(
#   total_infos, country_names, Confirmed_cases, cases_1M, Recovered_cases, death_cases
# )


def infos_to_lists():
    global names, total_infos, country_names, Confirmed_cases, cases_1M, Recovered_cases, death_cases
    country_names.clear()
    Confirmed_cases.clear()
    cases_1M.clear()
    Recovered_cases.clear()
    death_cases.clear()
    nm = 1
    cc = 5
    c_1M = 6
    rc = 7
    dc = 8
    for i in range(len(total_infos)):
        try:
            country_names.append(names[nm])
            Confirmed_cases.append(total_infos[cc])
            cases_1M.append(total_infos[c_1M])
            Recovered_cases.append(total_infos[rc])
            death_cases.append(total_infos[dc])
            nm += 1
            cc += 5
            c_1M += 5
            rc += 5
            dc += 5
        except IndexError:
            break


def get_url(urll):
    def get_text_from_html(info, list2):
        for ele in info:
            for w in ele:
                list2.append(w)

    total_infos.clear()
    names.clear()
    page = requests.get(urll)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("tbody", {"class": "ppcUXd"})
    # Country info
    counties_names = results.find_all("div", class_="pcAJd")
    counties_total = results.find_all("td", class_="l3HOY")
    get_text_from_html(counties_names, names)
    get_text_from_html(counties_total, total_infos)


def get_countries_special_info(url1, list_of_names, additional_list, flag_list):
    page = requests.get(url1)
    soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find("tbody", {"class": "ppcUXd"})
    result = results.find_all("tr", {"class": "sgXwHf wdLSAe YvL7re"})
    country_flags = results.find_all("img", {"class": "oIC36d"})
    for resultt in result:
        name_country = resultt.find("div", class_="pcAJd")
        list_of_names.append(name_country.text)
        additional_list.append(resultt["data-id"])
    for flag in country_flags:
        print(flag["src"])
        flag_list.append(flag["src"])


def remove_unimportant(first_list, url_all, list_no_sp_ch, url_list):
    num = 0
    for char in first_list:
        try:
            list_no_sp_ch.append(char.replace(char[0] + char[1] + char[2], ""))
            url_list.append(url_all + list_no_sp_ch[num])
            num += 1
        except IndexError:
            break


def url_to_picture(index, flag_list, label_tk):
    img_url = flag_list[index]
    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    label_tk["image"] = img
    label_tk.image = img


def window_list_countries():
    win = tk.Tk()
    styl = ThemedStyle()
    styl.set_theme("breeze")
    win.title("Coronavirus cases")
    win.geometry("800x700")
    win.resizable(False, False)
    tkinter.messagebox.showwarning(
        title="Warning",
        message="You MUST have good internet connection in order to work properly!",
    )

    def get_index(event):
        cs = listbox.curselection()
        name_of_selected = listbox.get(cs)
        if name_of_selected in name_countries:
            index = name_countries.index(name_of_selected)
            scroll.destroy()
            listbox.destroy()
            site = all_url[index]
            lbl = ttk.Label(
                win, text=random.choice(text_lbl_list), foreground="#30B1EC",
            )
            lbl.place(x=400, y=40, anchor=tk.CENTER)
            for i in range(21):
                progress["value"] = i
                win.update_idletasks()
                time.sleep(0.05)

            lbl["text"] = random.choice(text_lbl_list)
            print(site)
            get_url(site)
            for i in range(21, 41):
                progress["value"] = i
                win.update_idletasks()
                time.sleep(0.05)
            lbl["text"] = random.choice(text_lbl_list)
            infos_to_lists()
            for i in range(41, 61):
                progress["value"] = i
                win.update_idletasks()
                time.sleep(0.05)
            lbl["text"] = random.choice(text_lbl_list)
            print(
                country_names, Confirmed_cases, cases_1M, Recovered_cases, death_cases
            )
            for i in range(61, 81):
                progress["value"] = i
                win.update_idletasks()
                time.sleep(0.05)
            lbl["text"] = "Loading {} data".format(name_of_selected)
            for i in range(81, 101):
                progress["value"] = i
                win.update_idletasks()
                time.sleep(0.05)
            win.title("{} | Coronavirus statistics".format(name_of_selected))
            lbl.after(500, lbl.destroy())
            widgets(win, index + 1, name_of_selected)

    progress = ttk.Progressbar(
        win, orient=tk.HORIZONTAL, length=500, mode="determinate", value=0
    )
    scroll = ttk.Scrollbar(win)
    listbox = tk.Listbox(win, height=42)
    for i in range(len(name_countries)):
        listbox.insert(i, name_countries[i])

    listbox.config(yscrollcommand=scroll.set)
    scroll.config(command=listbox.yview)
    listbox.bind("<Double-1>", get_index)

    progress.pack(fill=tk.X)
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    listbox.pack(fill=tk.BOTH)
    win.mainloop()


def widgets(win, index, country):
    def county_to_country_coords(event):
        cs = listbox.curselection()
        name_of_selected = listbox.get(cs)
        if name_of_selected in country_names:
            index = country_names.index(name_of_selected)
            print(index)
            lbl_country_section["text"] = "County"
            lbl_country_name["text"] = country_names[index]
            lbl_total_cases["text"] = Confirmed_cases[index]
            lbl_cases_per1M["text"] = cases_1M[index]
            lbl_recovered_cases["text"] = Recovered_cases[index]
            lbl_dead_cases["text"] = death_cases[index]

    font = tkfont.Font(size=19)
    font2 = tkfont.Font(size=14)
    # Parent frames
    Frame_section_country_name = ttk.Frame(win)
    Frame_section_total_cases = ttk.Frame(win)
    Frame_section_1M_cases = ttk.Frame(win)
    Frame_section_recovered = ttk.Frame(win)
    Frame_section_deaths = ttk.Frame(win)
    Frame_listbox = ttk.Frame(win)
    # Children frames
    frame_section_confirmed = ttk.Frame(Frame_section_total_cases)
    frame_confirmed_cases = ttk.Frame(Frame_section_total_cases)
    frame_country_name_flag = ttk.Frame(Frame_section_country_name)
    frame_section_country = ttk.Frame(Frame_section_country_name)
    frame_section_per1M = ttk.Frame(Frame_section_1M_cases)
    frame_cases_per_1M = ttk.Frame(Frame_section_1M_cases)
    frame_section_recovered = ttk.Frame(Frame_section_recovered)
    frame_recovered_cases = ttk.Frame(Frame_section_recovered)
    frame_section_deaths = ttk.Frame(Frame_section_deaths)
    frame_dead_cases = ttk.Frame(Frame_section_deaths)
    # labels & stuff..
    # scroll = ttk.Scrollbar(Frame_listbox)
    listbox = tk.Listbox(Frame_listbox, height=33, font=font2)
    lbl_section_deaths = ttk.Label(
        frame_section_deaths, text="Deaths: ", font=font, foreground="red3"
    )
    lbl_dead_cases = ttk.Label(
        frame_dead_cases, text="{}".format(death_cases[0]), font=font, foreground="red3"
    )

    lbl_section_recovered = ttk.Label(
        frame_section_recovered,
        text="Recovered cases: ",
        font=font,
        foreground="forest green",
    )
    lbl_recovered_cases = ttk.Label(
        frame_recovered_cases,
        text="{}".format(Recovered_cases[0]),
        font=font,
        foreground="forest green",
    )

    lbl_section_1M = ttk.Label(
        frame_section_per1M, text="Cases per 1M: ", font=font, foreground="orange"
    )
    lbl_cases_per1M = ttk.Label(
        frame_cases_per_1M,
        text="{}".format(cases_1M[0]),
        font=font,
        foreground="orange",
    )

    lbl_flag = ttk.Label(frame_country_name_flag, image="", background="white")
    url_to_picture(index, flags_url_all, lbl_flag)
    lbl_country_name = ttk.Label(
        frame_country_name_flag, text="{}".format(country), font=font
    )
    lbl_section_confirm = ttk.Label(
        frame_section_confirmed, text="Total cases: ", font=font, foreground="gold2"
    )
    lbl_total_cases = ttk.Label(
        frame_confirmed_cases,
        text="{}".format(Confirmed_cases[0]),
        font=font,
        foreground="gold2",
    )

    lbl_country_section = ttk.Label(
        frame_section_country, text="Country's name: ", font=font
    )

    for i in range(len(country_names)):
        try:
            listbox.insert(i, country_names[i + 1])
        except IndexError:
            break
    listbox.bind("<Double-1>", county_to_country_coords)
    # Packing Frames
    Frame_section_country_name.pack(anchor=tk.NW, pady=4)
    Frame_section_total_cases.pack(anchor=tk.NW, pady=4)
    Frame_section_1M_cases.pack(anchor=tk.NW, pady=4)
    Frame_section_recovered.pack(anchor=tk.NW, pady=4)
    Frame_section_deaths.pack(anchor=tk.NW, pady=4)
    Frame_listbox.pack(pady=10, fill=tk.X)
    # Packing frames
    frame_section_country.pack(side=tk.LEFT, anchor=tk.NW)
    frame_country_name_flag.pack(side=tk.LEFT, anchor=tk.NW)
    frame_section_confirmed.pack(side=tk.LEFT, anchor=tk.NW)
    frame_confirmed_cases.pack(side=tk.LEFT, anchor=tk.NW)
    frame_section_per1M.pack(side=tk.LEFT, anchor=tk.NW)
    frame_cases_per_1M.pack(side=tk.LEFT, anchor=tk.NW)
    frame_section_recovered.pack(side=tk.LEFT, anchor=tk.NW)
    frame_recovered_cases.pack(side=tk.LEFT, anchor=tk.NW)
    frame_section_deaths.pack(side=tk.LEFT, anchor=tk.NW)
    frame_dead_cases.pack(side=tk.LEFT, anchor=tk.NW)
    # packing children of frames
    lbl_flag.pack(side=tk.LEFT, padx=5)
    lbl_country_name.pack(side=tk.LEFT, padx=5)
    lbl_section_confirm.pack(side=tk.LEFT, padx=5)
    lbl_total_cases.pack(side=tk.LEFT, padx=5)
    lbl_country_section.pack(pady=5)
    lbl_section_1M.pack(side=tk.LEFT, padx=5)
    lbl_cases_per1M.pack(side=tk.LEFT, padx=5)
    lbl_section_recovered.pack(side=tk.LEFT, padx=5)
    lbl_recovered_cases.pack(side=tk.LEFT, padx=5)
    lbl_section_deaths.pack(side=tk.LEFT, padx=5)
    lbl_dead_cases.pack(side=tk.LEFT, padx=5)
    listbox.pack(fill=tk.X)
    win.mainloop()


get_countries_special_info(url_all, name_countries, additional_name, flags_url_all)
remove_unimportant(additional_name, url, no_add_sp_char, all_url)
window_list_countries()
