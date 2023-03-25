'''
import pandas as pd
import numpy as np
import random
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout

#Config.set('graphics', 'width', '450')
#Config.set('graphics', 'height', '1000')

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from calendar import monthrange
from datetime import date, timedelta  # datetime
'''
from calendar import monthrange
from datetime import date, timedelta

import kivy
import pandas as pd
import random
# from kivy import Config
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager


# Config.set('graphics', 'width', '450')
# Config.set('graphics', 'height', '1000')

def today_question():
    # questions = pd.read_csv('data/questions_list.csv')
    # ques_id = random.randint(0, len(questions) - 1) + 1
    # today_ques = questions.loc[ques_id - 1, 'english']
    ques_id = random.randint(0, 10) + 1
    today_ques = str(ques_id)
    return today_ques, ques_id


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):
    pass


class HistoryWindow(Screen):
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    days_in_month = monthrange(year, month)[1]

    if month == 1:
        month_name = 'January'
    elif month == 2:
        month_name = 'February'
    elif month == 3:
        month_name = 'March'
    elif month == 4:
        month_name = 'April'
    elif month == 5:
        month_name = 'May'
    elif month == 6:
        month_name = 'June'
    elif month == 7:
        month_name = 'July'
    elif month == 8:
        month_name = 'August'
    elif month == 9:
        month_name = 'September'
    elif month == 10:
        month_name = 'October'
    elif month == 11:
        month_name = 'November'
    else:
        month_name = 'December'

    today_text = month_name + ' ' + str(year)


class SelectDayLayout(RelativeLayout):
    pass


class CalendarBox(GridLayout):
    cols = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(monthrange(date.today().year, date.today().month)[1]):
            b = SelectDayLayout()
            self.add_widget(b)

            day = date.today().replace(day=1) + timedelta(days=i)

            b.ids.date.text = day.strftime('%m/%d')

            b.ids.question.text = 'question'

            b.ids.mood.source = 'images/moods/happy.png'


class QnAWindow(Screen):
    mood = StringProperty('')

    def on_slider_value(self, widget):
        if widget.value < 20:
            self.mood = 'sad'
        elif widget.value < 40:
            self.mood = 'negative'
        elif widget.value < 60:
            self.mood = 'normal'
        elif widget.value < 80:
            self.mood = 'positive'
        else:
            self.mood = 'happy'

    question, ques_id = today_question()


class SettingWindow(Screen):
    pass


'''
def today_question():
    questions = pd.read_csv('data/questions_list.csv')
    ques_id = random.randint(0, len(questions) - 1) + 1
    today_ques = questions.loc[ques_id - 1, 'english']
    return today_ques, ques_id


# answers_list = pd.DataFrame(columns=['id', 'date', 'question', 'answer', 'mood'])
# answers_list.to_csv('user/answers_list.csv', sep=',', na_rep='NaN', index=False)
answers_list = pd.read_csv('user/answers_list.csv')


class QnAWindow(Screen):
    mood = StringProperty('')

    def on_slider_value(self, widget):

        if widget.value < 20:
            self.mood = 'sad'
        elif widget.value < 40:
            self.mood = 'negative'
        elif widget.value < 60:
            self.mood = 'normal'
        elif widget.value < 80:
            self.mood = 'positive'
        else:
            self.mood = 'happy'

    question, ques_id = today_question()
    answer = ''

    def set_answer(self, ans):
        self.answer = ans
        self.ids.answer.text = self.answer
        self.ids.answer.size_hint = (0.75, 0.05) if self.width < self.height else (0.3, 0.05)

        global answers_list
        # datetime.today().strftime('%Y-%m-%d')

        if len(answers_list[answers_list.date == str(date.today())]) == 0:
            answers_list = answers_list.append(
                {'id': self.ques_id, 'date': str(date.today()), 'question': self.question,
                 'answer': self.answer, 'mood': self.mood},
                ignore_index=True)
        else:
            answers_list.loc[
                answers_list.date == str(date.today()), ['id', 'question', 'answer', 'mood']] \
                = [self.ques_id, self.question, self.answer, self.mood]
        print(answers_list)
        answers_list.to_csv('user/answers_list.csv', sep=',', na_rep='NaN', index=False)

    def save_answer(self):
        global answers_list

        if len(answers_list[answers_list.date == str(date.today())]) == 0:
            answers_list = answers_list.append(
                {'id': self.ques_id, 'date': str(date.today()), 'question': self.question,
                 'answer': self.answer, 'mood': self.mood},
                ignore_index=True)
        else:
            answers_list.loc[
                answers_list.date == str(date.today()), ['id', 'question', 'answer', 'mood']] \
                = [self.ques_id, self.question, self.answer, self.mood]
        print(answers_list)
        answers_list.to_csv('user/answers_list.csv', sep=',', na_rep='NaN', index=False)


class HistoryWindow(Screen):
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    if month == 1:
        month_name = 'January'
    elif month == 2:
        month_name = 'February'
    elif month == 3:
        month_name = 'March'
    elif month == 4:
        month_name = 'April'
    elif month == 5:
        month_name = 'May'
    elif month == 6:
        month_name = 'June'
    elif month == 7:
        month_name = 'July'
    elif month == 8:
        month_name = 'August'
    elif month == 9:
        month_name = 'September'
    elif month == 10:
        month_name = 'October'
    elif month == 11:

        month_name = 'November'
    else:
        month_name = 'December'

    today_text = month_name + ' ' + str(year)


class SelectDayHistory(Screen):
    mood = 'normal'
    question = 'question'
    answer = 'answer'

    def access_history(self, select_date):
        day = "2023-{month}-{day}".format(month=select_date[0:2], day=select_date[3:5])

        if len(answers_list[answers_list['date'] == day]) != 0:
            self.question = answers_list[answers_list['date'] == day].question.iloc[0]
        else:
            self.question = ''

        if len(answers_list[answers_list['date'] == day]) != 0 and \
                answers_list[answers_list['date'] == day].answer.iloc[0] is not np.NaN:
            self.answer = answers_list[answers_list['date'] == day].answer.iloc[0]
        else:
            self.answer = ''

        if len(answers_list[answers_list['date'] == day]) != 0 and \
                answers_list[answers_list['date'] == day].mood.iloc[0] is not np.NaN:
            self.mood = answers_list[answers_list['date'] == day].mood.iloc[0]
        else:
            self.mood = ''

        self.ids.last_question.text = self.question
        self.ids.last_answer.text = self.answer
        if self.mood == '':
            self.ids.last_mood.color = (1, 1, 1, 0)
        else:
            self.ids.last_mood.source = 'images/moods/' + self.mood + '.png'


# class SelectDayButton(Button):
#    pass
class SelectDayLayout(RelativeLayout):
    pass


class CalendarBox(GridLayout):
    cols = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(monthrange(date.today().year, date.today().month)[1]):
            b = SelectDayLayout()
            self.add_widget(b)

            day = date.today().replace(day=1) + timedelta(days=i)

            b.ids.date.text = day.strftime('%m/%d')

            if len(answers_list[answers_list['date'] == str(day)]) != 0:
                question = answers_list[answers_list['date'] == str(day)].question.iloc[0]
            else:
                question = ''
            b.ids.question.text = question

            if len(answers_list[answers_list['date'] == str(day)]) != 0 and \
                    answers_list[answers_list['date'] == str(day)].mood.iloc[0] is not np.NaN:
                mood = answers_list[answers_list['date'] == str(day)].mood.iloc[0]
            else:
                mood = ''
            if mood == '':

                # b.ids.mood.source = 'images/moods/normal.png'
                b.ids.mood.color = (1, 1, 1, 0)
            else:
                b.ids.mood.source = 'images/moods/' + mood + '.png'

            if question == '':
                b.ids.select_btn.disabled = True


class SettingWindow(Screen):
    pass
'''


class RunApp(App):
    # def build(self):
    #    return kv
    pass


runApp = RunApp()
runApp.run()
