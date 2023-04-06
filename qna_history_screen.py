import csv

from kivy.app import App
from kivy.uix.screenmanager import Screen

# History QnA screen
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

    # get the size of answer chat box
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
