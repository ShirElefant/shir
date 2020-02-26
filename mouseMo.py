from tkinter import RIGHT
from unittest.mock import right

import pygame

LEFT = 1
running = 1
MIDDLE=2
RIGHT=3
SCROLLUP=4
SCROLLDOWN=5
scren = pygame.display.set_mode((400, 400))

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
         running = 0
         #press and relase of left button mouse
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        print ("You pressed the left mouse button at (%d, %d)" % event.pos)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
        print ("You released the left mouse button at (%d, %d)" % event.pos)
        # press and relase of right button mouse
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
        print("You pressed the right mouse button at (%d, %d)" % event.pos)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
        print ("You released the right mouse button at (%d, %d)" % event.pos)
        # press and relase of middle button mouse
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MIDDLE:
        print("You pressed the middle mouse button at (%d, %d)" % event.pos)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == MIDDLE:
        print ("You released the middle mouse button at (%d, %d)" % event.pos)
        # press and relase of scroll up mouse
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == SCROLLUP:
        print("You scrolled up with mouse at (%d, %d)" % event.pos)
  #  elif event.type == pygame.MOUSEBUTTONUP and event.button == SCROLLUP:
       # print ("You released the scroll up mouse button at (%d, %d)" % event.pos)
        # press and relase of scroll down mouse
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == SCROLLDOWN:
        print("You  scrolled up with mouse at (%d, %d)" % event.pos)
    # event.type == pygame.MOUSEBUTTONUP and event.button == SCROLLDOWN:
       # print ("You released the scroll down mouse button at (%d, %d)" % event.pos)

    scren.fill((0, 0, 0))
    pygame.display.flip()