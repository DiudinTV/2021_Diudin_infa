import turtle as t
t.speed(0)
t.color("cyan")
vx = 20
vy = 50
ay = -10
x = 0
y = 0
dt = 0.02
for i in range(9999):
    vy += ay * dt
    x += vx * dt
    y += vy * dt + ay * dt**2 / 2
    vx *= 0.99999
    t.goto(x, y)
    if y <= 0:
        y *= -1
        vy *= -0.8
        vx *= 0.8
