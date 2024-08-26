import pygame, sys
import random
from objects import Ball

pygame.init()


WIDTH = 1000
HEIGHT = 800
gravity = 1.0

border_width = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps = 60
clock = pygame.time.Clock()

objects = []

def draw_borders():
    top = pygame.draw.line(screen, 'white', (0, 0), (WIDTH, 0), border_width)
    left = pygame.draw.line(screen, 'white', (0, 0), (0, HEIGHT), border_width)
    right = pygame.draw.line(screen, 'white', (WIDTH, 0), (WIDTH, HEIGHT), border_width)
    bottom = pygame.draw.line(screen, 'white', (0, HEIGHT), (WIDTH, HEIGHT), border_width)
    borders = [top, left, right, bottom]
    return borders

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                objects.append(Ball(random.randint(10, 50), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], random.randrange(-50, 50, 1) / 10, 0, 0.5, 0.833, 0, random.randrange(-100, -1, 1) / 100))

    screen.fill((0, 0, 0))
    for instance in objects:
        instance.handle_movement()
        instance.draw_self(screen)
    screen_borders = draw_borders()

    clock.tick(fps)
    pygame.display.update()

