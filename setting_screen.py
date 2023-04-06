import csv

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen


class SettingWindow(Screen):
    settings = None
    with open('setting.csv', 'r', newline='') as file:
        setting = csv.reader(file)
        settings = next(setting)

    language = settings[0]

    def music_setting(self, widget):
        if widget.active:
            # turn on/off music by switch value
            App.get_running_app().background_music.volume = 1
            # save into setting file
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow([settings[0], 'on', settings[2]])
        else:
            App.get_running_app().background_music.volume = 0
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow([settings[0], 'off', settings[2]])

    def sound_setting(self, widget):
        if widget.active:
            # turn on/off effect sound by switch value
            App.get_running_app().switch_screen.volume = 1
            App.get_running_app().click.volume = 0.5
            # save into setting file
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow([settings[0], settings[1], 'on'])
        else:
            App.get_running_app().switch_screen.volume = 0
            App.get_running_app().click.volume = 0
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow([settings[0], settings[1], 'off'])

    # English language change button
    def eng_setting(self, widget):
        if widget.state == 'down':
            self.ids.kor_btn.state = 'normal'
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow(['english', settings[1], settings[2]])
        else:
            self.ids.kor_btn.state = 'down'
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow(['korean', settings[1], settings[2]])

    # Korean language change button
    def kor_setting(self, widget):
        if widget.state == 'down':
            self.ids.eng_btn.state = 'normal'
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow(['korean', settings[1], settings[2]])
        else:
            self.ids.eng_btn.state = 'down'
            settings = None
            with open('setting.csv', 'r', newline='') as file:
                setting = csv.reader(file)
                settings = next(setting)

            with open('setting.csv', 'w', newline='') as file:
                setting = csv.writer(file)
                setting.writerow(['english', settings[1], settings[2]])


# Popup when language is changed
class SettingPopup(RelativeLayout):
    popup_opacity_eng = NumericProperty(0, rebind=True)
    popup_opacity_kor = NumericProperty(0, rebind=True)

    def show_popup_eng(self, btn):
        if btn.state == 'down':
            self.ids.popup_eng.color = (0, 0, 0, 1)
            self.popup_opacity_eng = 0.3
            Clock.schedule_once(self.hide_popup_eng, 2.5)

    def hide_popup_eng(self, dt):
        self.ids.popup_eng.color = (0, 0, 0, 0)
        self.popup_opacity_eng = 0

    def show_popup_kor(self, btn):
        if btn.state == 'down':
            self.ids.popup_kor.color = (0, 0, 0, 1)
            self.popup_opacity_kor = 0.3
            Clock.schedule_once(self.hide_popup_kor, 2.5)

    def hide_popup_kor(self, dt):
        self.ids.popup_kor.color = (0, 0, 0, 0)
        self.popup_opacity_kor = 0
