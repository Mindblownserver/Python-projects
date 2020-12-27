from datetime import datetime
from random import randint
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, OptionProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.list import (ILeftBodyTouch, IRightBodyTouch,
                             OneLineAvatarIconListItem)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDThemePicker, MDTimePicker
from kivymd.uix.screen import Screen
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.tab import MDTabsBase
from plyer import notification

clicked = []
Notified = []
Imma = []
since = []
checked = []
Can_notify = False
# Loading


class Loading(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.loading, 5)

    def loading(self, *args):
        data = JsonStore("Userinfo.json")
        state = data.get("First-time")["Is_opened"]
        Isopened = state
        print(Isopened)
        if Isopened == "False":
            self.parent.current = "First_scrn"
            data.get("First-time")["Is_opened"] = "True"
            data["First-time"] = data["First-time"]
        elif Isopened == "True":
            self.parent.current = "Main"


# Carousel effect

class First(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# The actual Tasks components

# -----> This class has refresh active tasks methode and date time remider <------


class Tab_active(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, *args):
        self.ids.list.clear_widgets()
        # Catching infos
        store = JsonStore("Userinfo.json")
        for key in store:
            if key != "First-time":
                if store.get(key)["Status"] == "Active":
                    self.ids.list.add_widget(
                        ListItemWithCheckboxActive(text=store.get(key)["Task"]))
            else:
                pass
        # This is the reminder Logic
        today = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime("%H:%M")
        for key in store:
            if key != "First-time":
                if store.get(key)["Date"] == "" or store.get(key)["Date"] == "{}".format(today) and store.get(key)["Status"] == "Active":

                    if store.get(key)["Time"] != "":

                        if store.get(key)["Time"] == time and key not in Notified and store.get(key)["Status"] == "Active" and Can_notify == True:
                            notification.notify(title="Turbo| {} task".format(
                                key), message="{} {} !".format(store.get(key)["Details"], store.get(key)[Time]), app_icon="Logo.png")
                            Notified.append(key)
                            # print(Notified)
                        else:
                            print(Can_notify)
                    else:
                        pass
                elif store.get(key)["Status"] == "Active":
                    #print("Task {} is for another day :)".format(key))
                    pass
        Clock.schedule_once(self.start, 3)


class Tab_completed(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, *args):
        self.ids.scroll.clear_widgets()
        # Catching infos
        store = JsonStore("Userinfo.json")
        for key in store:
            if key != "First-time":
                if store.get(key)["Status"] == "Completed":
                    self.ids.scroll.add_widget(
                        ListItemWithCheckboxCompleted(text="[s]{}[/s]".format(store.get(key)["Task"])))
            else:
                pass
        Clock.schedule_once(self.start, 3)


class ListItemWithCheckboxActive(OneLineAvatarIconListItem):

    def on_checkbox_Active(self, checkboxInstance, isActive):
        store = JsonStore("Userinfo.json")
        if isActive:
            #print("Checkbox Checked")
            #self.ids.check.active = False
            self.markup = True
            for key in sorted(store):
                if key != "First-time":
                    checked = store.get(key)["Task"]
                    if checked == self.text:
                        store.get(key)["Status"] = "Completed"
                        store[key] = store[key]
                        self.text = "[s]" + self.text + "[/s]"
                        toast("Task is completed")
        else:
            #self.text = self.text.replace("[s]", "").replace("[/s]", "")
            self.ids.check.active = True

    def go_to_edit(self):
        clicked.clear()
        data = JsonStore("Userinfo.json")
        self.text = self.text.replace("[s]", "").replace("[/s]", "")
        des = data.get(self.text)["Details"]
        date = data.get(self.text)["Date"]
        Time = data.get(self.text)["Time"]

        clicked.append(self.text)
        clicked.append(des)
        clicked.append(date)
        clicked.append(Time)
        # print(clicked[1])


class ListItemWithCheckboxCompleted(OneLineAvatarIconListItem):
    def on_checkbox_Active(self, checkboxInstance, isActive):
        if isActive:
            pass
        else:
            #self.text = self.text.replace("[s]", "").replace("[/s]", "")
            self.ids.checked.active = True


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class edit(ILeftBodyTouch, MDIconButton):
    pass


class RightSwitch(IRightBodyTouch, MDSwitch):
    pass


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        checked.clear()
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
        checked.append(self.text)


class ListItemWithSwitch(OneLineAvatarIconListItem):
    def switch_handler(self):
        global Can_notify
        if self.ids.sw.active == True:
            print("Switched")
            Can_notify = True
        else:
            print("Inactive")
            Can_notify = False
# Here it finishes


class Tasks_tabs(Screen):
    def __init__(self, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)
        Clock.schedule_once(self.start)

    def start(self, *args):
        tab1 = self.ids.tab_container
        tab2 = self.ids.tab_container
        tab1.add_widget(Tab_active(
            text="Active" if MainApp.language == "EN" else "Actifs"))
        tab2.add_widget(Tab_completed(
            text="Completed" if MainApp.language == "EN" else "Terminées"))

        menu_items = [
            {"text": "Settings" if MainApp.language == "EN" else "Paramètres"}]
        self.menu = MDDropdownMenu(
            caller=self.ids.tool,
            items=menu_items,
            width_mult=4,
        )
        self.menu.bind(on_release=self.menu_callback)

    def menu_callback(self, menu, item):
        print(item.text)
        print("Transfering..")
        self.menu.dismiss()
        self.parent.transition.direction = "left"
        self.parent.current = "settings"

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

# Create tasks screen


class Create(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_date(self, date):
        print(date.year)
        print(date.month)
        print(date.day)
        self.ids.Date.text = "{}-{}-{}".format(date.year, date.month, date.day)

    def get_time(self, instance, time):
        print(time)
        print(time.hour)
        print(time.minute)
        self.ids.time.text = "{}:{}".format(time.hour, time.minute)

    def date_picker(self):
        now = datetime.now().strftime('%Y:%m:%d')
        min_date = datetime.strptime(now, '%Y:%m:%d').date()
        date_dialog = MDDatePicker(callback=self.get_date, min_date=min_date)
        date_dialog.open()

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def cancel(self):
        self.ids.Date.text = ""
        self.ids.time.text = ""
        self.ids.name.text = ""
        self.ids.des.text = ""

    def create(self):
        if self.ids.name.text == "":
            toast("Please give a name")
        else:
            # Storing data of task in JSON
            store = JsonStore("Userinfo.json")
            try:
                if store[self.ids.name.text]:
                    print("Already in!")
                    store.put("{}({})".format(self.ids.name.text, len(store.keys())), Task="{}({})".format(self.ids.name.text, len(
                        store.keys())), Details=self.ids.des.text, Date=self.ids.Date.text, Time=self.ids.time.text, Status="Active")
            except KeyError:
                store.put(self.ids.name.text, Task=self.ids.name.text, Details=self.ids.des.text,
                          Date=self.ids.Date.text, Time=self.ids.time.text, Status="Active")
            toast("Task created successfully!")
        self.ids.Date.text = ""
        self.ids.time.text = ""
        self.ids.name.text = ""
        self.ids.des.text = ""

# Settings screen


class sets(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)
        Clock.schedule_once(self.setup)

    def Github(self, *args):
        print("Githubbed")

    # Account make
    def setup(self, *args):
        print(Imma[0], since[0])
        self.ids.usr.text += f"{Imma[0]}"
        self.ids.usr.secondary_text += f"{since[0]}"

    def start(self, *args):
        completed = []

        data = JsonStore("Userinfo.json")
        for key in sorted(data):
            if key != "First-time":
                if data.get(key)["Status"] == "Completed":
                    completed.append(key)
        self.ids.num.text = f"Completed tasks: {len(completed)}" if MainApp.language == "EN" else f"{len(completed)} tâches terminées"
        Clock.schedule_once(self.start, 4)

    def get_color(self):
        store = JsonStore("Theme.json")
        Crl = self.ids.theme.text_color
        print(Crl)
        Red = [0.9568627450980393, 0.2627450980392157, 0.21176470588235294, 1]
        Green = [0.2980392156862745, 0.6862745098039216, 0.3137254901960784, 1]
        Blue = [0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1]
        Pink = [0.9137254901960784, 0.11764705882352941, 0.38823529411764707, 1]
        Purple = [0.611764705882353,
                  0.15294117647058825, 0.6901960784313725, 1]
        DeepPurple = [0.403921568627451,
                      0.22745098039215686, 0.7176470588235294, 1]
        Indigo = [0.24705882352941178,
                  0.3176470588235294, 0.7098039215686275, 1]
        LightBlue = [0.011764705882352941,
                     0.6627450980392157, 0.9568627450980393, 1]
        Cyan = [0.0, 0.7372549019607844, 0.8313725490196079, 1]
        Teal = [0.0, 0.5882352941176471, 0.5333333333333333, 1]
        LightGreen = [0.5450980392156862,
                      0.7647058823529411, 0.2901960784313726, 1]
        Lime = [0.803921568627451, 0.8627450980392157, 0.2235294117647059, 1]
        Yellow = [1.0, 0.9215686274509803, 0.23137254901960785, 1]
        Amber = [1.0, 0.7568627450980392, 0.027450980392156862, 1]
        Orange = [1.0, 0.596078431372549, 0.0, 1]
        DeepOrange = [1.0, 0.3411764705882353, 0.13333333333333333, 1]
        Brown = [0.4745098039215686, 0.3333333333333333, 0.2823529411764706, 1]
        Gray = [0.6196078431372549, 0.6196078431372549, 0.6196078431372549, 1]
        BlueGray = [0.3764705882352941,
                    0.49019607843137253, 0.5450980392156862, 1]
        if Crl == Red:
            print("Red")
            store.get("Theme")["color"] = "Red"
            store["Theme"] = store['Theme']
        elif Crl == Green:
            print("Green")
            store.get("Theme")["color"] = "Green"
            store["Theme"] = store['Theme']
        elif Crl == Blue:
            print("Blue")
            store.get("Theme")["color"] = "Blue"
            store["Theme"] = store['Theme']
        elif Crl == Pink:
            print("Pink")
            store.get("Theme")["color"] = "Pink"
            store["Theme"] = store['Theme']
        elif Crl == Purple:
            print("Purple")
            store.get("Theme")["color"] = "Purple"
            store["Theme"] = store['Theme']
        elif Crl == DeepPurple:
            print("DeepPurple")
            store.get("Theme")["color"] = "DeepPurple"
            store["Theme"] = store['Theme']
        elif Crl == Indigo:
            print("Indigo")
            store.get("Theme")["color"] = "Indigo"
            store["Theme"] = store['Theme']
        elif Crl == LightBlue:
            print("LightBlue")
            store.get("Theme")["color"] = "LightBlue"
            store["Theme"] = store['Theme']
        elif Crl == Cyan:
            print("Cyan")
            store.get("Theme")["color"] = "Cyan"
            store["Theme"] = store['Theme']
        elif Crl == Teal:
            print("Teal")
            store.get("Theme")["color"] = "Teal"
            store["Theme"] = store['Theme']
        elif Crl == LightGreen:
            print("LightGreen")
            store.get("Theme")["color"] = "LightGreen"
            store["Theme"] = store['Theme']
        elif Crl == Lime:
            print("Lime")
            store.get("Theme")["color"] = "Lime"
            store["Theme"] = store['Theme']
        elif Crl == Yellow:
            print("Yellow")
            store.get("Theme")["color"] = "Yellow"
            store["Theme"] = store['Theme']
        elif Crl == Amber:
            print("Green")
            store.get("Theme")["color"] = "Amber"
            store["Theme"] = store['Theme']
        elif Crl == Orange:
            print("Orange")
            store.get("Theme")["color"] = "Orange"
            store["Theme"] = store['Theme']
        elif Crl == DeepOrange:
            print("DeepOrange")
            store.get("Theme")["color"] = "DeepOrange"
            store["Theme"] = store['Theme']
        elif Crl == Brown:
            print("Brown")
            store.get("Theme")["color"] = "Brown"
            store["Theme"] = store['Theme']
        elif Crl == Gray:
            print("Gray")
            store.get("Theme")["color"] = "Gray"
            store["Theme"] = store['Theme']
        elif Crl == BlueGray:
            print("BlueGray")
            store.get("Theme")["color"] = "BlueGray"
            store["Theme"] = store['Theme']

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def callback(self, text, widget):
        print(text)

    def show_alert_dialog(self):
        self.dialog = MDDialog(
            title="Warning" if MainApp.language == "EN" else "Attention",
            text="This process will remove all your progress such as N° tasks, etc..." if MainApp.language == "EN" else "Ce processus supprimera tous vos progrès tels que N ° tâches, etc ...",
            auto_dismiss=False,
            size_hint=(0.7, 1),
            buttons=[
                MDFlatButton(
                    text="CANCEL" if MainApp.language == "EN" else "Annuler", text_color=(0, 0, 1, 1), on_release=lambda x: self.dialog_handler(x)
                ),
                MDRaisedButton(
                    text="OK", text_color=(1, 1, 1, 1), on_release=lambda x: self.dialog_handler(x)
                ),
            ],
        )
        self.dialog.open()

    def dialog_handler(self, widget):
        if widget.__class__.__name__ == "MDFlatButton":
            print("Canceled")
            self.dialog.dismiss()
        else:
            print("Delete")
            self.dialog.dismiss()
            store = JsonStore("Userinfo.json")
            store.clear()
            store.clear()
            data = JsonStore("Theme.json")
            data.clear()
            data.clear()
            exit()

    def show_lang_dialogue(self):
        self.dialog = MDDialog(
            title="Languages" if MainApp.language == "EN" else "langue",
            auto_dismiss=False,
            size_hint=(0.7, 1),
            type="confirmation",
            items=[
                ItemConfirm(text="English" if MainApp.language ==
                            "EN" else "Anglais"),
                ItemConfirm(text="French" if MainApp.language ==
                            "EN" else "Français"),
            ],
            buttons=[
                MDFlatButton(
                    text="CANCEL" if MainApp.language == "EN" else "Annuler", text_color=(0, 0, 1, 1), on_release=lambda x: self.lang_dialogue_handler(x)
                ),
                MDRaisedButton(
                    text="OK", text_color=(1, 1, 1, 1), on_release=lambda x: self.lang_dialogue_handler(x)
                ),
            ],
        )
        self.dialog.open()

    def lang_dialogue_handler(self, widget):
        store = JsonStore("Theme.json")
        if widget.__class__.__name__ == "MDFlatButton":
            print("Canceled")
            self.dialog.dismiss()
        else:
            if checked[0] == "English" or checked[0] == "Anglais":
                MainApp.language = "EN"
                print(checked[0])
                store.put("language", lang="EN")
                toast("Please restart to apply changes")
            elif checked[0] == "French" or checked[0] == "Français":
                print(checked[0])
                MainApp.language = "FR"
                store.put("language", lang="FR")
                toast("Veuillez redémarrer pour appliquer les modifications")
            self.dialog.dismiss()
# Editing screen


class Geeze(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, *args):

        if len(clicked) > 0:
            self.ids.Title.title = f"{clicked[0]} | Task" if MainApp.language == "EN" else f"{clicked[0]} | Tâche"
            if self.ids.des.text != "" or self.ids.Date.text != "" or self.ids.time.text != "":
                pass
            else:
                self.ids.des.text = clicked[1]
                self.ids.Date.text = clicked[2]
                self.ids.time.text = clicked[3]
        Clock.schedule_once(self.start)

    def get_date(self, date):
        print(date.year)
        print(date.month)
        print(date.day)
        self.ids.Date.text = "{}-{}-{}".format(date.year, date.month, date.day)

    def get_time(self, instance, time):
        print(time)
        print(time.hour)
        print(time.minute)
        self.ids.time.text = "{}:{}".format(time.hour, time.minute)

    def date_picker(self):
        now = datetime.now().strftime('%Y-%m-%d')
        min_date = datetime.strptime(now, '%Y-%m-%d').date()
        if self.ids.Date.text != "":
            date = datetime.strptime(self.ids.Date.text, "%Y-%m-%d").date()
            Year = date.year
            Month = date.month
            Day = date.day
        else:
            date = ""
            Year = ""
            Month = ""
            Day = ""
        date_dialog = MDDatePicker(
            callback=self.get_date, min_date=min_date, year=Year, month=Month, day=Day)
        date_dialog.open()

    def time_picker(self):
        time_dialog = MDTimePicker()
        if self.ids.time.text != "":
            previous_time = datetime.strptime(
                self.ids.time.text, '%H:%M').time()
            time_dialog.set_time(previous_time)
        else:
            pass
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def edited(self):
        store = JsonStore("Userinfo.json")
        store.get(clicked[0])["Details"] = self.ids.des.text
        store.get(clicked[0])["Date"] = self.ids.Date.text
        store.get(clicked[0])["Time"] = self.ids.time.text
        store[clicked[0]] = store[clicked[0]]
        # This where it ends
        self.ids.des.text = ""
        self.ids.Date.text = ""
        self.ids.time.text = ""
        toast(f"Edited >{clicked[0]}<" if MainApp.language ==
              "EN" else f">{clicked[0]}< est éditée")
        clicked.clear()

    def cancel(self):
        self.ids.des.text = ""
        self.ids.Date.text = ""
        self.ids.time.text = ""
        toast(f"Canceled >{clicked[0]}<" if MainApp.language ==
              "EN" else f">{clicked[0]}< est annulée")
        clicked.clear()

# Where the Main app begins


class MainApp(MDApp):
    language = OptionProperty('EN', options=('EN', 'FR'))
    try:
        store = JsonStore("Theme.json")
        language = store.get("language")["lang"]
    except:
        store = JsonStore("Theme.json")
        store.put("language", lang="EN")
        language = "EN"

    def build(self):
        self.win = Builder.load_file("Main.kv")
        try:
            store = JsonStore("Theme.json")
            color = store.get("Theme")["color"]
            self.theme_cls.primary_palette = color
            data = JsonStore("Userinfo.json")
            state = data.get("First-time")["Is_opened"]
            if state == "True":
                # print("True")
                Isopened = True
            else:
                Isopened = False
        except KeyError:
            data = JsonStore("Userinfo.json")
            self.theme_cls.primary_palette = "Red"
            store.put("Theme", color=self.theme_cls.primary_palette)
            data.put("First-time", Is_opened="False")
        finally:
            try:
                Imma.clear()
                since.clear()
                immatricule = JsonStore("Theme.json").get("Setts")["Num"]
                Since = JsonStore("Theme.json").get("since")["Since"]
                Imma.append(immatricule)
                since.append(Since)
            except:
                file = JsonStore("Theme.json")
                Imma.clear()
                since.clear()
                num = randint(0, 99999)
                now = datetime.now().strftime('%Y-%m-%d')
                now = datetime.strptime(now, '%Y-%m-%d').date()
                Imma.append(num)
                since.append(now.year)
                file.put("Setts", Num=num)
                file.put("since", Since=now.year)
        return self.win


MainApp().run()
