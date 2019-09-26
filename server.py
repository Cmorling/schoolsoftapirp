from flask import Flask
import main

app = Flask(__name__)
student=main.schoolsoft("caspian.morling", "C4sp14nM0rl1ng_schoolsoft")
student.login()
@app.route('/food')
def hello_world():
    menu=student.get_food()
    menuString = "The food for today is: "
    for i in menu:
        menuString = menuString + i + ", "
    menuString = menuString[:-2]
    return menuString
