import turtle as t

n = int(input())
t.shape("turtle")
for i in range(n):
    t.forward(50)
    t.stamp()
    t.right(90)
    t.stamp()
    t.left(180)
    t.stamp()
    t.left(90)
    t.stamp()
    t.forward(50)
    t.right(180 + (360 / n))
