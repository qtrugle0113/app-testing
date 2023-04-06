import csv
from datetime import date, datetime
import random

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

questions = []
# load questions list
with open('data/questions_list.csv', 'r') as file:
    questions_list = csv.reader(file)
    for row in questions_list:
        questions.append(row)


# load/create question
def today_question():
    # load language
    settings = None
    with open('setting.csv', 'r', newline='') as file:
        setting = csv.reader(file)
        settings = next(setting)
    # language mode: 2 for english, 1 for korean
    lang_mode = 2 if settings[0] == 'english' else 1

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


class QnAWindow(Screen):
    previous_screen = 'main'  # use for saving previous screen
    is_popup_open = False  # boolean using to avoid user back to previous screen when popup is being opened

    ques_id, question, answer, mood, mood_value = today_question()
    mood = StringProperty(mood)
    if mood_value == '':
        mood_value = 100
    today = date.today()

    # get slider value to convert to moods
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

    # set size of answer chat box initial
    def get_answerbox_size(self):
        break_line_count = self.answer.count('\n')  # count break line symbol
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

    # resize answer chat box when user input answer and save answer when user click "Answer" popup button
    def set_answer(self, ans):
        self.answer = ans
        self.ids.answer.text = self.answer
        break_line_count = self.answer.count('\n')  # count break line symbol

        # resize answer chat box
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

        # load answers list
        answers = []
        with open('user/answers_list.csv', 'r') as file:
            answers_list = csv.reader(file)
            for row in answers_list:
                answers.append(row)

        is_answered = False
        # write user's answer to answers_list file
        for i in range(len(answers)):  # backward search
            if answers[len(answers) - i - 1][1] == str(self.today):
                answers[len(answers) - i - 1] = [self.ques_id, str(self.today), self.question, self.answer, self.mood,
                                                 int(self.mood_value)]
                is_answered = True

        # write new answer_list file with new answer is added
        if is_answered:
            with open('user/answers_list.csv', 'w', newline='') as file:
                new_list = csv.writer(file)
                new_list.writerows(answers)
        # append new question to answers_list file with blank answer
        else:
            with open('user/answers_list.csv', 'a', newline='') as file:
                answers_list = csv.writer(file)
                answers_list.writerow(
                    [self.ques_id, str(self.today), self.question, self.answer, self.mood, int(self.mood_value)])

    # save answer when user choose mood on mood slider
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
