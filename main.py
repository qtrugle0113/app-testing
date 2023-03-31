from calendar import monthrange
from datetime import date, datetime, timedelta

# import kivy
# import pandas as pd
# import numpy as np
import random
import csv
from kivy import Config
from kivy.app import App
# from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '1000')
from kivy.core.window import Window


def today_question():
    questions = []
    # load questions list
    with open('data/questions_list.csv', 'r') as file:
        questions_list = csv.reader(file)
        for row in questions_list:
            questions.append(row)

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
            today_ques = answers[i][2]
            today_ans = answers[i][3]
            today_mood = answers[i][4]
            mood_value = answers[i][5]
            return ques_id, today_ques, today_ans, today_mood, mood_value

    # if not created, randomly pick a question from questions list
    ques_id = random.randint(1, len(questions) - 1)
    # prevent the same question will be created within 60days
    while True:
        diff_days = 9999  # the days between 2 same questions if they are created, initially set as a large number
        for row in range(len(answers) - 1):
            # backward loop, not execute label row
            if int(answers[len(answers) - row - 1][0]) == ques_id:  # check random created question is exist
                date_before = datetime.strptime(answers[len(answers) - row - 1][1], '%Y-%m-%d')
                date_now = datetime.strptime(str(today), '%Y-%m-%d')
                diff_days = (date_now - date_before).days
                break  # for loop break

        if diff_days > 60:  # within 60 days, the same question will not be created
            break  # while loop break
        # try to random a another question
        ques_id = random.randint(1, len(questions) - 1)

    today_ques = questions[ques_id][2]
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
            elif self.current_screen.name == "qna":
                self.current = "main"
                self.transition.direction = 'right'
                return True  # do not exit the app
            elif self.current_screen.name == "history":
                self.current = "main"
                self.transition.direction = 'right'
                return True  # do not exit the app
            elif self.current_screen.name == "qna_history":
                self.current = "history"
                self.transition.direction = 'right'
                return True  # do not exit the app
            elif self.current_screen.name == "setting":
                self.current = "main"
                self.transition.direction = 'right'
                return True  # do not exit the app


class MainWindow(Screen):
    pass


class HistoryWindow(Screen):
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    days_in_month = monthrange(year, month)[1]

    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    today_text = months[month] + ' ' + str(year)

    def change_month(self, action):
        if action == 'previous':
            if self.month == 1:
                self.month = 12
                self.year = self.year - 1
            else:
                self.month = self.month - 1
        else:
            if self.month == 12:
                self.month = 1
                self.year = self.year + 1
            else:
                self.month = self.month + 1

        self.today_text = self.months[self.month] + ' ' + str(self.year)
        self.ids.select_month.text = self.today_text
        self.days_in_month = monthrange(self.year, self.month)[1]
        # resize scroll screen
        self.ids.calendar_box.height = 250 * self.days_in_month
        self.ids.calendar_box.change_calendar(self.month, self.year)
        print(self.month, self.year)



class SelectDayLayout(RelativeLayout):
    canvas_opacity_line = NumericProperty(1, rebind=True)
    canvas_opacity_button = NumericProperty(0.4, rebind=True)
    canvas_opacity_border = NumericProperty(0, rebind=True)


class CalendarBox(GridLayout):
    cols = 1
    today = date.today()

    def change_calendar(self, new_month, new_year):
        for i in range(31):
        #for i in range(monthrange(new_year, new_month)[1]):
            day = self.today.replace(year=new_year, month=new_month, day=1) + timedelta(days=i)

            if i >= monthrange(new_year, new_month)[1]:
                self.ids[i + 1].size_hint = (0, 0)
                self.ids[i + 1].ids.date.text = ''
                self.ids[i + 1].ids.question.text = ''
                self.ids[i + 1].ids.mood.color = (1, 1, 1, 0)
                self.ids[i + 1].canvas_opacity_line = 0
                self.ids[i + 1].canvas_opacity_button = 0
                self.ids[i + 1].canvas_opacity_border = 0
                continue

            self.ids[day.day].canvas_opacity_line = 1
            self.ids[day.day].canvas_opacity_button = 0.4
            #self.ids[day.day].canvas_opacity_border = 0

            self.ids[day.day].size_hint = (1, 0.25)
            self.ids[day.day].ids.date.text = day.strftime('%m/%d')
            #self.ids[day.day].ids.date.text = 'ok'
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
                self.ids[day.day].ids.select_btn.bind(on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna'))
            else:
                self.ids[day.day].canvas_opacity_border = 0
                self.ids[day.day].ids.select_btn.bind(
                    on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna_history'))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #for i in range(monthrange(self.today.year, self.today.month)[1]):
        for i in range(31):
            day = self.today.replace(day=1) + timedelta(days=i)

            if i >= monthrange(self.today.year, self.today.month)[1]:
                b = SelectDayLayout()
                self.ids[i + 1] = b
                #b.size_hint = (1, 0.25)
                b.size_hint = (0, 0)
                b.ids.mood.color = (1, 1, 1, 0)
                b.canvas_opacity_line = 0
                self.add_widget(b)
                continue
            #day = self.today.replace(day=1) + timedelta(days=i)
            b = SelectDayLayout()
            #self.ids[day] = b
            self.ids[day.day] = b
            self.add_widget(b)

            b.ids.date.text = day.strftime('%m/%d')

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
                b.ids.select_btn.bind(on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna'))
            else:
                b.ids.select_btn.bind(
                    on_release=lambda *args: setattr(App.get_running_app().root, 'current', 'qna_history'))

    def update_data(self, today_ques, today_mood):
        '''self.ids[self.today].ids.select_btn.disabled = False
        self.ids[self.today].ids.question.text = today_ques
        if today_mood == '':
            self.ids[self.today].ids.mood.source = 'images/moods/normal.png'
            self.ids[self.today].ids.mood.color = (1, 1, 1, 0)
        else:
            self.ids[self.today].ids.mood.source = 'images/moods/' + today_mood + '.png'
            self.ids[self.today].ids.mood.color = (1, 1, 1, 1)'''
        self.ids[self.today.day].ids.select_btn.disabled = False
        self.ids[self.today.day].ids.question.text = today_ques
        if today_mood == '':
            self.ids[self.today.day].ids.mood.source = 'images/moods/normal.png'
            self.ids[self.today.day].ids.mood.color = (1, 1, 1, 0)
        else:
            self.ids[self.today.day].ids.mood.source = 'images/moods/' + today_mood + '.png'
            self.ids[self.today.day].ids.mood.color = (1, 1, 1, 1)


class QnAWindow(Screen):
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

    def set_answer(self, ans):
        self.answer = ans
        self.ids.answer.text = self.answer
        self.ids.answer.size_hint = (0.75, 0.05)

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


class QnAHistoryWindow(Screen):
    mood = 'normal'
    question = ''
    answer = ''
    mood_value = 0

    def access_history(self, select_date):
        day = "2023-{month}-{day}".format(month=select_date[0:2], day=select_date[3:5])
        # load answers list data
        answers = []
        with open('user/answers_list.csv', 'r') as file:
            answers_list = csv.reader(file)
            for row in answers_list:
                answers.append(row)
        # find qna data for day
        for i in range(len(answers)):
            if answers[i][1] == day:
                self.question = answers[i][2]
                self.answer = answers[i][3]
                self.mood = answers[i][4]
                self.mood_value = answers[i][5]
                break

        self.ids.last_question.text = self.question
        self.ids.last_answer.text = self.answer
        if self.mood_value == '':
            self.mood_value = 100
        self.ids.last_mood_slider.value = self.mood_value
        if self.mood == '':
            self.ids.last_mood.source = 'images/moods/normal.png'
            self.ids.last_mood.color = (1, 1, 1, 0)
            self.ids.last_mood_slider.value_track_color = [0.8, 0.1, 0.9, 0]
        else:
            self.ids.last_mood.source = 'images/moods/' + self.mood + '.png'
            self.ids.last_mood.color = (1, 1, 1, 1)
            self.ids.last_mood_slider.value_track_color = [0.8, 0.1, 0.9, 0.4]


class SettingWindow(Screen):
    pass


class RunApp(App):
    # def build(self):
    #    return kv
    pass


runApp = RunApp()
runApp.run()
