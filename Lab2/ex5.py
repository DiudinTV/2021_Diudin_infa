import turtle as t

for i in range(10):
    for j in range(4):
        t.forward(10 * (i + 1))
        t.right(90)
    t.penup()
    t.goto(-5 * (i + 1), 5 * (i + 1))
    t.pendown()
