import turtle as t
import numpy as np


def okr(r, a):
    t.right(a)
    for i in range(360):
        t.forward(r * 2 * np.pi / 360)
        t.right(1)
    t.left(a)


t.speed(0)
for j in range(6):
    okr(60, j * 60)
