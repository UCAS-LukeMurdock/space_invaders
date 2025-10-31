# LM  Space Invaders Game

import pygame
import random

# initializing pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")

# 32x32 image icon
pygame_icon = pygame.image.load('resources/ufo-1.png')
pygame.display.set_icon(pygame_icon)

# Player Class
class Player:
    def __init__(self, x, change = 0):
        self.img = pygame.image.load('resources/spaceship.png')
        self.x = x
        self.y = 600-69
        self.change = change
    
    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= (800-64):
            self.x = 736

class Enemy:
    def __init__(self, x, y, change = 0):
        self.img = pygame.image.load('resources/alien.png')
        self.x = x
        self.y = 600-69
        self.change = change
        

player = Player(370)

running = True
while running:
    screen.fill((0,0,0))

    # loop events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.3
            if keys[pygame.K_RIGHT]:
                player.change = 0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
    
    # Changes
    player.move()

    # Set Items
    player.player_set()


    
    pygame.display.flip()