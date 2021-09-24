import turtle as t
import numpy as np

N = open("rnd3.txt", "r")
N = N.read().split()
q = input()
x = -400
t.penup()
t.goto(x, 0)
t.pendown()
t.speed(0)
t.color("red")
for i in q:
    for el in (N[int(i)]):
        if el == "1":
            t.forward(40)
        elif el == "2":
            t.right(45)
        elif el == "3":
            t.left(45)
        elif el == "4":
            t.right(180)
        elif el == "5":
            t.forward(40 * np.sqrt(2))
        elif el == "6":
            t.penup()
            t.goto(x, -40)
            t.pendown()
        else:
            x += 50
            t.penup()
            t.goto(x, 0)
            t.pendown()
