import random as rnd
import turtle as t
t.color("green")
t.speed(0)
for i in range(10000):
    t.forward(20*rnd.random())
    t.left(360*rnd.random())
