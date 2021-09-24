import turtle as t
import numpy as np


def okr(r, a):
    t.right(a)
    for p in range(90):
        t.forward(r * 2 * np.pi / 90)
        t.right(4)
    t.left(a)


t.speed(0)
t.left(90)
for i in range(10):
    okr(7 * (i + 1), 0)
    okr(7 * (i + 1), 180)
