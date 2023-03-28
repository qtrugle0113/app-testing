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
from kivy.properties import StringProperty
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

    for i in range(len(answers)):
        if answers[i][1] == str(date.today()):
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
                date_now = datetime.strptime(str(date.today()), '%Y-%m-%d')
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
        answers_list.writerow([ques_id, str(date.today()), today_ques, today_ans, today_mood, mood_value])
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
            day = date.today().replace(day=1) + timedelta(days=i)

            b = SelectDayLayout()
            self.ids[day] = b
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

            if day != date.today() and (question == '' or (answer == '' and mood == '')):
                b.ids.select_btn.disabled = True

            #if day == date.today():
            #    b.bind(on_release=self.switch_screen)

    #def switch_screen(self, *args):
    #    runApp.screen_manager.current.current = 'qna'

    def update_data(self, today_ques, today_mood):
        self.ids[date.today()].ids.select_btn.disabled = False
        self.ids[date.today()].ids.question.text = today_ques
        if today_mood == '':
            self.ids[date.today()].ids.mood.source = 'images/moods/normal.png'
            self.ids[date.today()].ids.mood.color = (1, 1, 1, 0)
        else:
            self.ids[date.today()].ids.mood.source = 'images/moods/' + today_mood + '.png'
            self.ids[date.today()].ids.mood.color = (1, 1, 1, 1)


class QnAWindow(Screen):
    ques_id, question, answer, mood, mood_value = today_question()
    mood = StringProperty(mood)
    if mood_value == '':
        mood_value = 100

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
            if answers[len(answers) - i - 1][1] == str(date.today()):
                answers[len(answers) - i - 1] = [self.ques_id, str(date.today()), self.question, self.answer, self.mood,
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
                    [self.ques_id, str(date.today()), self.question, self.answer, self.mood, int(self.mood_value)])

    def save_answer(self, touch, widget):
        if touch.grab_current == widget:
            answers = []
            with open('user/answers_list.csv', 'r') as file:
                answers_list = csv.reader(file)
                for row in answers_list:
                    answers.append(row)

            is_answered = False

            for i in range(len(answers)):
                if answers[len(answers) - i - 1][1] == str(date.today()):
                    answers[len(answers) - i - 1] = [self.ques_id, str(date.today()), self.question, self.answer,
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
                        [self.ques_id, str(date.today()), self.question, self.answer, self.mood, int(self.mood_value)])


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
