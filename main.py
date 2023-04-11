# Use for debugging: start
from kivy import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '1024')
# Use for debugging: end

from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# import code from another py files: start
from qna_screen import *
from history_screen import *
from qna_history_screen import *
from setting_screen import *
import openai
# import code from another py files: end


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:  # the back button on android
            if self.current_screen.name == "main":
                return False  # exit the app from this page
            elif self.current_screen.name == "qna" and App.get_running_app().root.get_screen('qna').is_popup_open:
                return True  # keep screen and do not exit the app
            elif self.current_screen.name == "qna" and App.get_running_app().root.get_screen(
                    'qna').previous_screen == 'main':
                self.current = "main"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app
            elif self.current_screen.name == "qna" and App.get_running_app().root.get_screen(
                    'qna').previous_screen == 'history':
                self.current = "history"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app
            elif self.current_screen.name == "history":
                self.current = "main"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app
            elif self.current_screen.name == "ques_history" and App.get_running_app().root.get_screen(
                    'ques_history').previous_screen == 'qna':
                self.current = "qna"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app
            elif self.current_screen.name == "ques_history" and App.get_running_app().root.get_screen(
                    'ques_history').previous_screen == 'qna_history':
                self.current = "qna_history"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app
            elif self.current_screen.name == "qna_history":
                self.current = "history"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app
            elif self.current_screen.name == "setting":
                self.current = "main"
                self.transition.direction = 'right'
                App.get_running_app().switch_screen.play()
                return True  # do not exit the app


class MainWindow(Screen):
    pass


class RunApp(App):
    # load setting file
    settings = None
    with open('setting.csv', 'r', newline='') as file:
        setting = csv.reader(file)
        settings = next(setting)

    language = settings[0]
    music = 1 if settings[1] == 'on' else 0
    sound = 1 if settings[2] == 'on' else 0

    # init_audio
    # Background music:
    background_music = SoundLoader.load('audio/background.mp3')
    background_music.volume = 1 * music
    background_music.loop = True
    # Affect sound:
    # play when switching screens
    switch_screen = SoundLoader.load('audio/switch_sound.mp3')
    switch_screen.volume = 1 * sound
    # play when click button
    click = SoundLoader.load('audio/click(UNIVERSFIELD).mp3')
    click.volume = 0.5 * sound

    background_music.play()

    # animate logo in main screen
    init_pos_y = 0.6
    delta_pos_y = 0.0002
    delta_opa = 0.01
    tap_here_opacity = NumericProperty(0.3, rebind=True)

    def build(self):
        App.get_running_app().root.get_screen('main').ids.logo.pos_hint = {'center_x': 0.5, 'center_y': self.init_pos_y}
        Clock.schedule_interval(self.animate_logo, 1.0 / 60.0)

    def animate_logo(self, dt):
        if self.init_pos_y < 0.575 or self.init_pos_y > 0.6:
            self.delta_pos_y = -self.delta_pos_y

        if self.tap_here_opacity > 1 or self.tap_here_opacity < 0.1:
            self.delta_opa = -self.delta_opa

        self.tap_here_opacity += self.delta_opa
        self.init_pos_y -= self.delta_pos_y
        App.get_running_app().root.get_screen('main').ids.logo.pos_hint = {'center_x': 0.5, 'center_y': self.init_pos_y}


runApp = RunApp()
runApp.run()
