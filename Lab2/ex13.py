import turtle as t
import numpy as np


def dug(r, alpha):
    for _ in range(alpha):
        t.forward(r * 2 * np.pi / 360)
        t.right(1)


def okr(r, a):
    t.right(a)
    for _ in range(180):
        t.forward(r * 2 * np.pi / 180)
        t.right(2)
    t.left(a)


t.speed(0)
col = ["cyan", "light green"]

t.begin_fill()
okr(100, 0)
t.color("yellow")
t.end_fill()

for i in range(2):
    t.color("black")
    t.penup()
    t.goto(-40 + i * 80, -40)
    t.pendown()
    t.begin_fill()
    okr(20, 0)
    t.color(col[i])
    t.end_fill()

t.penup()
t.goto(0, -90)
t.pendown()

t.color("black")
t.width(5)
t.right(90)
t.forward(25)
t.left(135)
t.forward(10)

t.penup()
t.goto(45, -125)
t.pendown()

t.color("magenta")
t.width(20)
t.right(135)
dug(45, 180)
