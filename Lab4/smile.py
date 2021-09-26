import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

dr.rect(screen, (255, 255, 255), (0, 0, 500, 500))
dr.circle(screen, (255, 255, 0), (200, 200), 150)
dr.circle(screen, (255, 0, 0), (140, 150), 20)
dr.circle(screen, (255, 0, 0), (260, 150), 25)
dr.circle(screen, (0, 0, 0), (140, 155), 10)
dr.circle(screen, (0, 0, 0), (260, 160), 12)
dr.rect(screen, (0, 0, 0), (125, 250, 150, 25))
dr.line(screen, (0, 0, 0), (100, 100), (190, 150), 25)
dr.line(screen, (0, 0, 0), (300, 100), (210, 150), 30)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
