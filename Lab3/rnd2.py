import turtle as t
import numpy as np

t.color("magenta")


def zer():
    for i in range(2):
        t.forward(40)
        t.right(45)
        t.right(45)
        t.forward(40)
        t.forward(40)
        t.right(45)
        t.right(45)


def one():
    t.penup()
    t.right(45)
    t.right(45)
    t.forward(40)
    t.right(45)
    t.right(180)
    t.pendown()
    t.forward(40 * np.sqrt(2))
    t.right(45)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.forward(40)
    t.left(45)
    t.left(45)


def two():
    for i in range(2):
        t.forward(40)
        t.right(45)
        t.right(45)
    t.left(45)
    t.forward(40 * np.sqrt(2))
    t.right(45)
    t.right(180)
    t.forward(40)


def thr():
    t.forward(40)
    t.left(45)
    t.right(180)
    t.forward(40 * np.sqrt(2))
    t.right(45)
    t.right(180)
    t.forward(40)
    t.left(45)
    t.right(180)
    t.forward(40 * np.sqrt(2))
    t.right(45)
    t.right(180)


def fou():
    t.right(45)
    t.right(45)
    t.forward(40)
    t.left(45)
    t.left(45)
    t.forward(40)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.right(180)
    t.forward(40)
    t.forward(40)
    t.right(45)
    t.right(45)


def fiv():
    t.forward(40)
    t.right(180)
    t.forward(40)
    t.left(45)
    t.left(45)
    t.forward(40)
    t.left(45)
    t.left(45)
    t.forward(40)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.right(180)


def six():
    t.penup()
    t.forward(40)
    t.left(45)
    t.right(180)
    t.pendown()
    t.forward(40 * np.sqrt(2))
    t.left(45)
    t.forward(40)
    for _ in range(3):
        t.left(45)
        t.left(45)
        t.forward(40)
    t.right(180)


def sev():
    t.forward(40)
    t.left(45)
    t.right(180)
    t.forward(40 * np.sqrt(2))
    t.left(45)
    t.forward(40)
    t.left(45)
    t.left(45)


def eig():
    t.forward(40)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.forward(40)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.right(45)
    t.right(45)
    t.forward(40)
    t.forward(40)
    t.right(180)
    t.forward(40)
    t.left(45)
    t.left(45)
    t.forward(40)


def nin():
    for _ in range(5):
        t.forward(40)
        t.right(45)
        t.right(45)
    t.forward(40)
    t.right(45)
    t.forward(40 * np.sqrt(2))
    t.right(45)
    t.right(180)


t.penup()
t.goto(-400, 0)
t.pendown()
t.speed(0)
bank = [zer, one, two, thr, fou, fiv, six, sev, eig, nin]
num = input()
c = 0
for n in num:
    c += 1
    bank[int(n)]()
    t.penup()
    t.goto(50 * c - 400, 0)
    t.pendown()
