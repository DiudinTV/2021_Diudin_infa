import turtle as t
import numpy as np


def dug(r, alpha):
    for p in range(alpha):
        t.forward(r * 2 * np.pi / 360)
        t.right(1)


t.speed(0)
t.left(90)
for i in range(5):
    dug(20, 180)
    dug(5, 180)
