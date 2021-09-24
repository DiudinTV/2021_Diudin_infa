from random import randint
import turtle

number_of_turtles = 16
steps_of_time_number = 1000

pool = [[turtle.Turtle(shape='circle'), 0, 0, randint(-8, 8), randint(-8, 8)] for i in range(number_of_turtles)]
for unit in pool:
    unit[0].penup()
    unit[0].speed(0)
    unit[1] = randint(-300, 300)
    unit[2] = randint(-200, 200)
    unit[0].goto(unit[1], unit[2])
pool[0][0].goto(-310, -210)
pool[0][0].pendown()
for _ in range(2):
    pool[0][0].forward(620)
    pool[0][0].left(90)
    pool[0][0].forward(420)
    pool[0][0].left(90)
pool[0][0].penup()
pool[0][0].goto(pool[0][1], pool[0][2])

for i in range(steps_of_time_number):
    for unit in pool:
        unit[1] += unit[3]
        unit[2] += unit[4]
        if unit[1] > 300:
            unit[1] = 600 - unit[1]
            unit[3] *= -1
        elif unit[1] < -300:
            unit[1] = -600 - unit[1]
            unit[3] *= -1
        if unit[2] > 200:
            unit[2] = 400 - unit[2]
            unit[4] *= -1
        elif unit[2] < -200:
            unit[2] = -400 - unit[2]
            unit[4] *= -1
        unit[0].goto(unit[1], unit[2])
