from flask import Flask
import main

app = Flask(__name__)
student=main.schoolsoft("caspian.morling", "C4sp14nM0rl1ng_schoolsoft")
@app.route('/food')
def get_food():
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
@app.route('/monday')
def monday():
    day_schedule=student.get_schedule(0)
    menu_string = "The schedule for Monday is: "
    for i in day_schedule:
        menu_string = menu_string + i + ", "
    
    return menu_string
@app.route('/tuesday')
def tuesday():
    day_schedule=student.get_schedule(1)
    menu_string = "The schedule for Tuesday is: "
    for i in day_schedule:
        menu_string = menu_string + i + ", "
    
    return menu_string
@app.route('/wednesday')
def wednesday():
    day_schedule=student.get_schedule(2)
    menu_string = "The schedule for wednesday is: "
    for i in day_schedule:
        menu_string = menu_string + i + ", "
    
    return menu_string
@app.route('/thursday')
def thursday():
    day_schedule=student.get_schedule(3)
    menu_string = "The schedule for thrusday is: "
    for i in day_schedule:
        menu_string = menu_string + i + ", "
    
    return menu_string
@app.route('/friday')
def friday():
    day_schedule=student.get_schedule(4)
    menu_string = "The schedule for friday is: "
    for i in day_schedule:
        menu_string = menu_string + i + ", "
    
    return menu_string