import requests
import re
import email
import sys
import json
import datetime
from bs4 import BeautifulSoup
class subject:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.merits = 0
        self.grade = "Not tested"

    def new_grade(self, merit):
        if merit < 10:
            self.merits = 0
            self.grade = "F"

        elif merit >= 10 and merit < 12.5:
            self.merits = 10
            self.grade = "E"

        elif merit >= 12.5 and merit < 14.5:
            self.merits = 12.5
            self.grade = "D"

        elif merit >= 14.5 and merit < 17:
            self.merits = 15
            self.grade = "C"

        elif merit >= 17 and merit < 19.5:
            self.merits = 17.5
            self.grade = "B"

        elif merit >= 19.5 and merit <= 20:
            self.merits = 20
            self.grade = "A"

class grades:
    def __init__(self):
        self.art = subject("art", 6890)
        self.biology = subject("biology", 7219)
        self.chemestry = subject("chemestry", 7218)
        self.civics = subject("civics", 7217)
        self.english = subject("english", 6887)
        self.french = subject("french", 6886)
        self.geography = subject("geography", 7216)
        self.history = subject("history", 7215)
        self.hkk = subject("hkk", 9354)
        self.math = subject("math", 402)
        self.music = subject("music", 6883)
        self.physical_ed = subject("physical_ed", 6882)
        self.physics = subject("physics", 7214)
        self.religion = subject("religion", 7213)
        self.swedish = subject("swedish", 6878)
        self.technology = subject("technology", 7220)
        self.crafts = subject("crafts", 6888)

class schoolsoft:
    def __init__(self, username, password):
        self.user_creds = {
            "action": "login",
            "usertype": "1",
            "ssusername": username,
            "sspassword": password,
        }
        self.grades = grades()
        self.cookies ={}
        self.total_merits = 0
        self.latest_results = ""

    def login(self):
        r = requests.post("https://sms14.schoolsoft.se/engelska/jsp/Login.jsp", data=self.user_creds, cookies=self.cookies, allow_redirects=False)
        self.cookies = r.cookies
    '''
    def get_grades(self):
        r = requests.get('https://sms14.schoolsoft.se/engelska/jsp/student/right_student_gradesubject.jsp?menu=gradesubject', cookies=self.cookies)
        print(r.text)
    '''
    def get_subject(self, subject):
        '''Returns merits of subject and updates subject acording to knownledge requirements'''
        r = requests.get('https://sms14.schoolsoft.se/engelska/jsp/student/right_student_ability.jsp?subject=%s&schooltype=7' % subject.id, cookies=self.cookies)
        ordered_criteria = re.findall(r'"green"(?! style)|"yellow"(?! style)|"red"(?! style)|list&ability=', r.text)
        ordered_criteria.append("")

        subject_merit = 0
        subject_criteria = 0
        for index, val in enumerate(ordered_criteria):
            if val == "list&ability=" and (ordered_criteria[index + 1] == '"yellow"' or ordered_criteria[index + 1] == '"red"'):
                return 0
            elif val == "list&ability=" and ordered_criteria[index + 1] == '"green"':
                subject_criteria += 1
                subject_merit += 10
                if ordered_criteria[index + 2] == '"yellow"':
                    subject_merit += 2.5
                elif ordered_criteria[index + 2] == '"green"':
                    subject_merit += 5
                    if ordered_criteria[index + 3] == '"yellow"':
                        subject_merit += 2.5
                    elif ordered_criteria[index + 3] == '"green"':
                        subject_merit += 5

        merit = (subject_merit/subject_criteria)

        induvidual_subject = getattr(self.grades, subject.name)
        induvidual_subject.new_grade(merit)

        return merit
    def get_results(self):
        '''Fetches latest result'''
        r = requests.get("https://sms14.schoolsoft.se/engelska/jsp/student/right_student_test_results.jsp?subject=0", cookies=self.cookies)
        results = re.search(r'[A-Z]{2} - .[^<]+', r.text)
        print(results)

    def get_total_merit(self):
        for attr in dir(self.grades):
            if not attr.startswith('__'):
                '''Fetch the    '''
                s = getattr(self.grades, attr)
                '''Fetch from ss server to update local'''
                self.get_subject(s)
                '''Fetch from local and add upp merits'''
                self.total_merits += s.merits
                '''Get table'''
                print('%s: %s' % (s.name, s.grade))
    def get_food(self):
        r = requests.get("https://sms14.schoolsoft.se/engelska/jsp/student/right_student_lunchmenu.jsp?menu=lunchmenu", cookies=self.cookies)
        menu = BeautifulSoup(r.text, "html.parser")
        print(menu)
        lunch_menu = []

        for div in menu.find_all("td", {"style": "word-wrap: break-word"}):
            food_info = div.get_text(separator=u"<br/>").split(u"<br/>")
            lunch_menu.append(food_info)
        today = datetime.datetime.today().weekday()
        if today < 5:
            print(today, lunch_menu)
            return {'weekend': False, 'm': lunch_menu[today]}
        if today > 4:
            print(today, lunch_menu)
            return {'weekend': True, 'm': lunch_menu[4]}
