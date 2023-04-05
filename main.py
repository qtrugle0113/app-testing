from calendar import monthrange
from datetime import date, datetime, timedelta

import random
import csv
from kivy import Config
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
# from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '1000')
from kivy.core.window import Window

questions = []
# load questions list
with open('data/questions_list.csv', 'r') as file:
    questions_list = csv.reader(file)
    for row in questions_list:
        questions.append(row)


def today_question():
    # load language
    settings = None
    with open('setting.csv', 'r', newline='') as file:
        setting = csv.reader(file)
        settings = next(setting)
    # language mode: 2 for english, 1 for korean
    lang_mode = 2 if settings[0] == 'english' else 1

    """questions = []
    # load questions list
    with open('data/questions_list.csv', 'r') as file:
        questions_list = csv.reader(file)
        for row in questions_list:
            questions.append(row)"""

    # if already created, reload question data
    answers = []
    with open('user/answers_list.csv', 'r') as file:
        answers_list = csv.reader(file)
        for row in answers_list:
            answers.append(row)

    today = date.today()
    for i in range(len(answers)):
        if answers[i][1] == str(today):
            ques_id = answers[i][0]
            today_ques = questions[int(ques_id)][lang_mode]
            today_ans = answers[i][3]
            today_mood = answers[i][4]
            mood_value = answers[i][5]
            return ques_id, today_ques, today_ans, today_mood, mood_value

    # if not created, randomly pick a question from questions list
    ques_id = str(random.randint(1, len(questions) - 1))
    # prevent the same question will be created within 60days
    while True:
        diff_days = 9999  # the days between 2 same questions if they are created, initially set as a large number
        for row in range(len(answers) - 1):
            # backward loop, '-1' means not execute label row
            if answers[len(answers) - row - 1][0] == ques_id:  # check random created question is exist
                date_before = datetime.strptime(answers[len(answers) - row - 1][1], '%Y-%m-%d')
                date_now = datetime.strptime(str(today), '%Y-%m-%d')
                diff_days = (date_now - date_before).days
                break  # for loop break

        if diff_days > 60:  # within 60 days, the same question will not be created
            break  # while loop break
        # try to random another question
        ques_id = str(random.randint(1, len(questions) - 1))

    today_ques = questions[int(ques_id)][lang_mode]
    today_ans = ''
    today_mood = ''
    mood_value = ''
    # save question to answers list
    with open('user/answers_list.csv', 'a', newline='') as file:
        answers_list = csv.writer(file)
        answers_list.writerow([ques_id, str(today), today_ques, today_ans, today_mood, mood_value])
    return ques_id, today_ques, today_ans, today_mood, mood_value


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
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


class HistoryWindow(Screen):
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    days_in_month = monthrange(year, month)[1]
    today_text = None
    # set position for the scroll calendar box: 1 is top, 0 is bottom
    # scroll_view_pos = 1 - day/days_in_month
    scroll_view_pos = 1

    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    # load language
    settings = None
    with open('setting.csv', 'r', newline='') as file:
        setting = csv.reader(file)
        settings = next(setting)

    if settings[0] == 'english':
        today_text = months[month] + ' ' + str(year)
    else:
        today_text = str(year) + '년' + ' ' + str(month) + '월'

    def change_month(self, action):
        if action == 'previous':
            if self.month == 1:
                self.month = 12
                self.year = self.year - 1
            else:
                self.month = self.month - 1
        elif action == 'next':
            if self.month == 12:
                self.month = 1
                self.year = self.year + 1
            else:
                self.month = self.month + 1
        else:
            self.month = self.today.month
            self.year = self.today.year
        if self.settings[0] == 'english':
            self.today_text = self.months[self.month] + ' ' + str(self.year)
        else:
            self.today_text = str(self.year) + '년' + ' ' + str(self.month) + '월'

        self.ids.select_month.text = self.today_text
        self.days_in_month = monthrange(self.year, self.month)[1]
        # resize scroll screen
        self.ids.calendar_box.height = 250 * self.days_in_month
        self.ids.calendar_box.change_calendar(self.month, self.year)
        self.ids.scroll_box.scroll_y = 1
        # print(self.month, self.year)


class SelectDayLayout(RelativeLayout):
    canvas_opacity_line = NumericProperty(1, rebind=True)
    canvas_opacity_button = NumericProperty(0.4, rebind=True)
    canvas_opacity_border = NumericProperty(0, rebind=True)

    def screen_switch_setting(self, border):
        if border == 1:  # only 'today' row has a border
            return 'qna'
        else:
            return 'qna_history'


class CalendarBox(GridLayout):
    cols = 1
    today = date.today()
    weekdays = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU',
                4: 'FRI', 5: 'SAT', 6: 'SUN'}
    weekdays_kor = {0: '월', 1: '화', 2: '수', 3: '목',
                    4: '금', 5: '토', 6: '일'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # for i in range(monthrange(self.today.year, self.today.month)[1]):
        for i in range(31):
            day = self.today.replace(day=1) + timedelta(days=i)
            weekday_idx = (monthrange(self.today.year, self.today.month)[0] + i) % 7

            if i >= monthrange(self.today.year, self.today.month)[1]:
                b = SelectDayLayout()
                self.ids[i + 1] = b
                b.size_hint = (0, 0)
                b.ids.select_btn.disabled = True
                b.ids.mood.color = (1, 1, 1, 0)
                b.canvas_opacity_line = 0
                self.add_widget(b)
                continue
            # day = self.today.replace(day=1) + timedelta(days=i)
            b = SelectDayLayout()
            # self.ids[day] = b
            self.ids[day.day] = b
            self.add_widget(b)
            b.size_hint = (1, 0.25)
            b.ids.date.text = day.strftime('%m/%d')
            if App.get_running_app().language == 'english':
                b.ids.weekday.text = self.weekdays[weekday_idx]
            else:
                b.ids.weekday.text = self.weekdays_kor[weekday_idx]
            b.ids.year_saver.text = day.strftime('%Y')

            answers = []

            with open('user/answers_list.csv', 'r') as file:
                answers_list = csv.reader(file)
                for row in answers_list:
                    answers.append(row)

            question = ''
            answer = ''
            mood = ''
            for j in range(len(answers)):
                if answers[j][1] == str(day):
                    if App.get_running_app().language == 'english' and day == self.today:
                        question = questions[int(answers[j][0])][2]
                    elif App.get_running_app().language == 'korean' and day == self.today:
                        question = questions[int(answers[j][0])][1]
                    else:
                        question = answers[j][2]
                    answer = answers[j][3]
                    mood = answers[j][4]
                    break

            b.ids.question.text = question
            if mood == '':
                b.ids.mood.source = 'images/moods/normal.png'
                b.ids.mood.color = (1, 1, 1, 0)
            else:
                b.ids.mood.source = 'images/moods/' + mood + '.png'

            if day != self.today and (question == '' or (answer == '' and mood == '')):
                b.ids.select_btn.disabled = True
            # Move to QnA Screen if select date is today
            if day == self.today:
                b.canvas_opacity_border = 1
                # b.ids.select_btn.bind(on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna'))
            else:
                b.canvas_opacity_border = 0
                # b.ids.select_btn.bind(
                #    on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna_history'))

    def change_calendar(self, new_month, new_year):
        for i in range(31):
            # for i in range(monthrange(new_year, new_month)[1]):
            day = self.today.replace(year=new_year, month=new_month, day=1) + timedelta(days=i)
            weekday_idx = (monthrange(new_year, new_month)[0] + i) % 7

            if i >= monthrange(new_year, new_month)[1]:
                self.ids[i + 1].size_hint = (0, 0)
                self.ids[i + 1].ids.date.text = ''
                self.ids[i + 1].ids.weekday.text = ''
                self.ids[i + 1].ids.question.text = ''
                self.ids[i + 1].ids.year_saver.text = ''
                self.ids[i + 1].ids.select_btn.disabled = True
                self.ids[i + 1].ids.mood.color = (1, 1, 1, 0)
                self.ids[i + 1].canvas_opacity_line = 0
                self.ids[i + 1].canvas_opacity_button = 0
                self.ids[i + 1].canvas_opacity_border = 0
                continue

            self.ids[day.day].size_hint = (1, 0.25)
            self.ids[day.day].ids.date.text = day.strftime('%m/%d')
            if App.get_running_app().language == 'english':
                self.ids[day.day].ids.weekday.text = self.weekdays[weekday_idx]
            else:
                self.ids[day.day].ids.weekday.text = self.weekdays_kor[weekday_idx]
            self.ids[day.day].ids.year_saver.text = day.strftime('%Y')
            answers = []

            with open('user/answers_list.csv', 'r') as file:
                answers_list = csv.reader(file)
                for row in answers_list:
                    answers.append(row)

            question = ''
            answer = ''
            mood = ''

            for j in range(len(answers)):
                if answers[j][1] == str(day):
                    if App.get_running_app().language == 'english' and day == self.today:
                        question = questions[int(answers[j][0])][2]
                    elif App.get_running_app().language == 'korean' and day == self.today:
                        question = questions[int(answers[j][0])][1]
                    else:
                        question = answers[j][2]
                    answer = answers[j][3]
                    mood = answers[j][4]
                    break

            self.ids[day.day].ids.question.text = question
            if mood == '':
                self.ids[day.day].ids.mood.source = 'images/moods/normal.png'
                self.ids[day.day].ids.mood.color = (1, 1, 1, 0)
            else:
                self.ids[day.day].ids.mood.source = 'images/moods/' + mood + '.png'
                self.ids[day.day].ids.mood.color = (1, 1, 1, 1)

            if day != self.today and (question == '' or (answer == '' and mood == '')):
                self.ids[day.day].ids.select_btn.disabled = True
            else:
                self.ids[day.day].ids.select_btn.disabled = False
            # Move to QnA Screen if select date is today
            if day == self.today:
                self.ids[day.day].canvas_opacity_border = 1
                # self.ids[day.day].ids.select_btn.bind(
                #    on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna'))
            else:
                self.ids[day.day].canvas_opacity_border = 0
                # self.ids[day.day].ids.select_btn.bind(
                #    on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna_history'))

            self.ids[day.day].canvas_opacity_line = 1
            self.ids[day.day].canvas_opacity_button = 0.4

    def update_data(self, today_ques, today_mood):
        App.get_running_app().root.get_screen('history').change_month('now')

        self.ids[self.today.day].ids.select_btn.disabled = False
        self.ids[self.today.day].ids.question.text = today_ques
        if today_mood == '':
            self.ids[self.today.day].ids.mood.source = 'images/moods/normal.png'
            self.ids[self.today.day].ids.mood.color = (1, 1, 1, 0)
        else:
            self.ids[self.today.day].ids.mood.source = 'images/moods/' + today_mood + '.png'
            self.ids[self.today.day].ids.mood.color = (1, 1, 1, 1)


class QnAWindow(Screen):
    previous_screen = 'main'
    is_popup_open = False

    ques_id, question, answer, mood, mood_value = today_question()
    mood = StringProperty(mood)
    if mood_value == '':
        mood_value = 100
    today = date.today()

    def on_slider_value(self, widget):
        self.mood_value = widget.value
        if widget.value < 40:
            self.mood = 'sad'
        elif widget.value < 80:
            self.mood = 'negative'
        elif widget.value < 120:
            self.mood = 'normal'
        elif widget.value < 160:
            self.mood = 'positive'
        else:
            self.mood = 'happy'

    def get_answerbox_size(self):
        break_line_count = self.answer.count('\n')
        if len(self.answer) == 0:
            return (0, 0)
        elif len(self.answer) <= 3:
            return (0.2, 0.025 * break_line_count + 0.06)
        elif len(self.answer) <= 10:
            return (0.45, 0.025 * break_line_count + 0.06)
        elif len(self.answer) <= 20:
            return (0.65, 0.025 * break_line_count + 0.06)
        elif App.get_running_app().language == 'english':
            return (0.8, 0.025 * (int(len(self.answer) / 40) + break_line_count) + 0.06)
        else:
            return (0.8, 0.025 * (int(len(self.answer) / 30) + break_line_count) + 0.06)

    def set_answer(self, ans):
        self.answer = ans
        self.ids.answer.text = self.answer
        break_line_count = self.answer.count('\n')

        if len(self.answer) <= 3:
            self.ids.answer.size_hint = (0.2, 0.025 * break_line_count + 0.06)
        elif len(self.answer) <= 10:
            self.ids.answer.size_hint = (0.45, 0.025 * break_line_count + 0.06)
        elif len(self.answer) <= 20:
            self.ids.answer.size_hint = (0.65, 0.025 * break_line_count + 0.06)
        elif App.get_running_app().language == 'english':
            self.ids.answer.size_hint = (0.8, 0.025 * (int(len(self.answer) / 40) + break_line_count) + 0.06)
        else:
            self.ids.answer.size_hint = (0.8, 0.025 * (int(len(self.answer) / 30) + break_line_count) + 0.06)


        answers = []
        with open('user/answers_list.csv', 'r') as file:
            answers_list = csv.reader(file)
            for row in answers_list:
                answers.append(row)

        is_answered = False

        for i in range(len(answers)):  # backward search
            if answers[len(answers) - i - 1][1] == str(self.today):
                answers[len(answers) - i - 1] = [self.ques_id, str(self.today), self.question, self.answer, self.mood,
                                                 int(self.mood_value)]
                is_answered = True

        if is_answered:
            with open('user/answers_list.csv', 'w', newline='') as file:
                new_list = csv.writer(file)
                new_list.writerows(answers)
        else:
            with open('user/answers_list.csv', 'a', newline='') as file:
                answers_list = csv.writer(file)
                answers_list.writerow(
                    [self.ques_id, str(self.today), self.question, self.answer, self.mood, int(self.mood_value)])

    def save_answer(self, touch, widget):
        if touch.grab_current == widget:
            answers = []
            with open('user/answers_list.csv', 'r') as file:
                answers_list = csv.reader(file)
                for row in answers_list:
                    answers.append(row)

            is_answered = False

            for i in range(len(answers)):
                if answers[len(answers) - i - 1][1] == str(self.today):
                    answers[len(answers) - i - 1] = [self.ques_id, str(self.today), self.question, self.answer,
                                                     self.mood, int(self.mood_value)]
                    is_answered = True

            if is_answered:
                with open('user/answers_list.csv', 'w', newline='') as file:
                    new_list = csv.writer(file)
                    new_list.writerows(answers)
            else:
                with open('user/answers_list.csv', 'a', newline='') as file:
                    answers_list = csv.writer(file)
                    answers_list.writerow(
                        [self.ques_id, str(self.today), self.question, self.answer, self.mood, int(self.mood_value)])


class SelectQuestionHistory(RelativeLayout):
    canvas_background_color = NumericProperty(200 / 255, rebind=True)
    canvas_background_alpha = NumericProperty(0.4, rebind=True)


class QuestionHistory(Screen):
    previous_screen = 'qna'

    def last_answer(self, ques_id, ques):
        self.ids.ques_his.text = ques

        last_dates = ['', '', '', '', '']
        last_answers = ['', '', '', '', '']
        last_moods = ['', '', '', '', '']
        filled = 0
        answers = []
        with open('user/answers_list.csv', 'r') as file:
            answers_list = csv.reader(file)
            for row in answers_list:
                answers.append(row)

        for i in range(len(answers) - 1):  # '-1' means not execute label row
            if answers[len(answers) - i - 1][0] == ques_id:
                last_dates[filled] = answers[len(answers) - i - 1][1]
                last_answers[filled] = answers[len(answers) - i - 1][3]
                last_moods[filled] = answers[len(answers) - i - 1][4]
                if filled >= 4:
                    break
                else:
                    filled += 1
        # print(last_dates[0])
        for j in range(5):
            if last_dates[j] != '':
                self.ids[str(j)].ids.date.text = '{month}-{day}'.format(month=last_dates[j][5:7],
                                                                        day=last_dates[j][8:10])
                self.ids[str(j)].ids.year.text = '{year}'.format(year=last_dates[j][0:4])
                self.ids[str(j)].canvas_background_color = 200 / 255
                self.ids[str(j)].canvas_background_alpha = 0.4
            else:
                self.ids[str(j)].ids.date.text = ''
                self.ids[str(j)].ids.year.text = ''
                self.ids[str(j)].canvas_background_color = 100 / 255
                self.ids[str(j)].canvas_background_alpha = 0.8
            self.ids[str(j)].ids.answer.text = last_answers[j]
            if last_moods[j] == '':
                self.ids[str(j)].ids.mood.source = 'images/moods/normal.png'
                self.ids[str(j)].ids.mood.color = (1, 1, 1, 0)
            else:
                self.ids[str(j)].ids.mood.source = 'images/moods/' + last_moods[j] + '.png'
                self.ids[str(j)].ids.mood.color = (1, 1, 1, 1)


class QnAHistoryWindow(Screen):
    def access_history(self, select_date, select_year):
        day = "{year}-{month}-{day}".format(year=select_year, month=select_date[0:2], day=select_date[3:5])
        mood = 'normal'
        ques_id = ''
        question = ''
        answer = ''
        mood_value = 100
        # load answers list data
        answers = []
        with open('user/answers_list.csv', 'r') as file:
            answers_list = csv.reader(file)
            for row in answers_list:
                answers.append(row)
        # find qna data for day
        for i in range(len(answers)):
            if answers[i][1] == day:
                ques_id = answers[i][0]
                question = answers[i][2]
                answer = answers[i][3]
                mood = answers[i][4]
                mood_value = answers[i][5]
                break

        self.ids.ques_id_saver.text = ques_id
        self.ids.last_question.text = question
        self.ids.last_answer.text = answer
        if mood_value == '':
            mood_value = 100
        self.ids.last_mood_slider.value = mood_value
        if mood == '':
            self.ids.last_mood.source = 'images/moods/normal.png'
            self.ids.last_mood.color = (1, 1, 1, 0)
            self.ids.last_mood_slider.value_track_color = [0.8, 0.1, 0.9, 0]
        else:
            self.ids.last_mood.source = 'images/moods/' + mood + '.png'
            self.ids.last_mood.color = (1, 1, 1, 1)
            self.ids.last_mood_slider.value_track_color = [0.8, 0.1, 0.9, 0.4]

    def get_answerbox_size(self, answer):
        break_line_count = answer.count('\n')
        if len(answer) <= 3:
            return (0.2, 0.025 * break_line_count + 0.06)
        elif len(answer) <= 10:
            return (0.45, 0.025 * break_line_count + 0.06)
        elif len(answer) <= 20:
            return (0.65, 0.025 * break_line_count + 0.06)
        elif App.get_running_app().language == 'english':
            return (0.8, 0.025 * (int(len(answer) / 40) + break_line_count) + 0.06)
        else:
            return (0.8, 0.025 * (int(len(answer) / 30) + break_line_count) + 0.06)


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


class RunApp(App):
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


runApp = RunApp()
runApp.run()
