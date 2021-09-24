import turtle as t
import numpy as np

t.right(60)
for i in range(10):
    t.penup()
    t.goto(0, 10 * (i + 1))
    t.pendown()
    for j in range(i + 3):
        t.forward(20 * (i + 1) * np.sin(np.pi / (i + 3)))
        t.right(360 / (i + 3))
    t.left(- 90 * (i + 1) / (i + 3) + 90 * (i + 2) / (i + 4))
