
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
mouse_position_log = []

objects = []
active_selection = False

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
            if event.button == 3:
                objects.append(Ball(random.randint(30, 75), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, 0.2, 0.833, 0, 0))

            if event.button == 1:

                for instance in objects:
                    if instance.check_select(event.pos):
                        active_selection = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for instance in objects:
                    if instance.selected and active_selection:
                        active_selection = False
                        instance.release(mouse_position_log)

    if active_selection:
        if len(mouse_position_log) < 20:
            mouse_position_log.append(pygame.mouse.get_pos())
        else:
            mouse_position_log.pop(0)

    screen.fill((0, 0, 0))
    num_objects = len(objects)
    for i, instance in enumerate(objects):
        instance.handle_movement(pygame.mouse.get_pos())
        for j, other_instance in enumerate(objects):
            if j != i:
                 if instance.check_collisions(other_instance):
                     instance.resolve_collisions(other_instance)
        instance.check_border_collision()

        # Draw Methods
        instance.draw_self(screen)
        instance.draw_vector(screen)

    screen_borders = draw_borders()

    clock.tick(fps)
    pygame.display.update()
