import turtle as t


def star(n):
    for _ in range(n):
        t.forward(100)
        t.left((180 - (180 / n)) * (-1) ** n)


star(8)
t.penup()
t.goto(150, 0)
t.pendown()
star(9)
