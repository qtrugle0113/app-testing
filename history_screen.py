import csv
from calendar import monthrange
from datetime import date, timedelta

from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen

from qna_screen import questions


class HistoryWindow(Screen):
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    days_in_month = monthrange(year, month)[1]
    today_text = None
    scroll_view_pos = 1

    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    # load language
    settings = None
    with open('setting.csv', 'r', newline='') as file:
        setting = csv.reader(file)
        settings = next(setting)

    # set date text label match with app language
    if settings[0] == 'english':
        today_text = months[month] + ' ' + str(year)
    else:
        today_text = str(year) + '년' + ' ' + str(month) + '월'

    # change data when user change date in history screen
    def change_month(self, action):
        # when user choose previous month
        if action == 'previous':
            if self.month == 1:
                self.month = 12
                self.year = self.year - 1
            else:
                self.month = self.month - 1
        # when user choose next month
        elif action == 'next':
            if self.month == 12:
                self.month = 1
                self.year = self.year + 1
            else:
                self.month = self.month + 1
        # reload today data
        else:
            self.month = self.today.month
            self.year = self.today.year
        if self.settings[0] == 'english':
            self.today_text = self.months[self.month] + ' ' + str(self.year)
        else:
            self.today_text = str(self.year) + '년' + ' ' + str(self.month) + '월'

        self.ids.select_month.text = self.today_text
        self.days_in_month = monthrange(self.year, self.month)[1]
        # resize scroll screen: size for a day is 250
        self.ids.calendar_box.height = 250 * self.days_in_month
        self.ids.calendar_box.change_calendar(self.month, self.year)
        self.ids.scroll_box.scroll_y = 1


class SelectDayLayout(RelativeLayout):
    # opacity for canvases
    canvas_opacity_line = NumericProperty(1, rebind=True)
    canvas_opacity_button = NumericProperty(0.4, rebind=True)
    canvas_opacity_border = NumericProperty(0, rebind=True)

    # determine which screen will be switched to
    def screen_switch_setting(self, border):
        # switch to QnA screen when user click on today button
        if border == 1:  # only 'today' row has a border
            return 'qna'
        # switch to QnA history screen when user click on another day button
        else:
            return 'qna_history'


# scrollable area in History screen
class CalendarBox(GridLayout):
    cols = 1
    today = date.today()
    weekdays = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU',
                4: 'FRI', 5: 'SAT', 6: 'SUN'}
    weekdays_kor = {0: '월', 1: '화', 2: '수', 3: '목',
                    4: '금', 5: '토', 6: '일'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initial create 31 buttons correspond to 31 days of month
        for i in range(31):
            day = self.today.replace(day=1) + timedelta(days=i)
            weekday_idx = (monthrange(self.today.year, self.today.month)[0] + i) % 7

            # set day buttons that not appear in month to be invisible
            if i >= monthrange(self.today.year, self.today.month)[1]:
                b = SelectDayLayout()
                self.ids[i + 1] = b
                b.size_hint = (0, 0)
                b.ids.select_btn.disabled = True
                b.ids.mood.color = (1, 1, 1, 0)
                b.canvas_opacity_line = 0
                self.add_widget(b)
                continue

            b = SelectDayLayout()
            # Load data for per day
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
            else:
                b.canvas_opacity_border = 0

    # chane data when user change month
    def change_calendar(self, new_month, new_year):
        for i in range(31):
            day = self.today.replace(year=new_year, month=new_month, day=1) + timedelta(days=i)
            weekday_idx = (monthrange(new_year, new_month)[0] + i) % 7

            # set day buttons that not appear in month to be invisible
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

            # load date for per day
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
            else:
                self.ids[day.day].canvas_opacity_border = 0

            self.ids[day.day].canvas_opacity_line = 1
            self.ids[day.day].canvas_opacity_button = 0.4

    # reload current month history when user answer question in QnA screen and save user answer
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

        # create 5 boxes correspond to last 5 answers
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
