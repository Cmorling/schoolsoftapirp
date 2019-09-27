from flask import Flask
import main

app = Flask(__name__)
student=main.schoolsoft("caspian.morling", "C4sp14nM0rl1ng_schoolsoft")
student.login()
@app.route('/food')
def hello_world():
    menu=student.get_food()
    print(menu)
    if menu['weekend'] == False:
        menuString = "The food for today is: "
    if menu['weekend'] == True:
        menuString = "The food this Friday was: "
    for i in menu['m']:
        menuString = menuString + i + ", "
    menuString = menuString[:-2]
    return menuString
