# LM  Space Invaders Game

import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# Set up background
background = pygame.image.load('resources/background.jpg')
background = pygame.transform.scale(background, (800,600))

# Background music
mixer.music.load('resources/background.wav')
mixer.music.play(-1)

# Score Text
score_font = pygame.font.Font('freesansbold.ttf', 32) # Search for other ones on the internet with "fonts ttf files"

# Set up display
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")

# 32x32 image icon
pygame_icon = pygame.image.load('resources/ufo.png')
pygame.display.set_icon(pygame_icon)

class Bullet:
    def __init__(self, x=0, y=0):
        self.state = "ready"
        self.x = x
        self.y = y
        self.change = -1
        self.img = pygame.image.load('resources/bullet.png')
        self.rotated = pygame.transform.rotate(self.img, 90)

    def shoot(self):
        self.change = -1
        screen.blit(self.rotated, (self.x, self.y))
        
    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.state = "ready"

    

# Player Class
class Player:
    def __init__(self, x, change = 0):
        self.img = pygame.image.load('resources/spaceship.png')
        self.x = x
        self.y = 600-69
        self.change = change
        self.score = 0
    
    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        # Borders of screen
        if self.x <= 0:
            self.x = 0
        elif self.x >= (800-64):
            self.x = 736


class Enemy:
    def __init__(self, x, y):
        self.img = pygame.image.load('resources/alien.png')
        self.x = x
        self.y = y
        self.x_change = 0.2
        self.y_change = 20

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        # Borders of screen
        if self.x <= 0:
            self.x_change = 0.2
            self.y += self.y_change
        elif self.x >= (800-64):
            self.x_change = -0.2
            self.y += self.y_change

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + ((self.y - bullet.y)**2))
        if distance < 48: # the sum of half the width of the bullet and of the alien
            return True
        return False
    
    def lose(self):
        if self.y > 540:
            return True
        return False

    

def create_enemies(round):
    for i in range(round *2):
        x = random.randint(0,800-64)
        y = random.randint(0,300-64)
        enemies.append(Enemy(x,y))
    round += 1
    return round


round = 1

player = Player(370)
bullet = Bullet()
enemies = []
round = create_enemies(round)

game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_txt = game_over_font.render(f"GAME OVER", True, (255,255,255))
game_over = False


running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    score_display = score_font.render(f"Round: {round}  |  Score: {player.score}", True, (255,255,255))
    screen.blit(score_display, (10,10))

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
            if keys[pygame.K_SPACE]:
                if bullet.state == "ready":
                    bullet.x = player.x +16
                    bullet.y = player.y +10
                    bullet.state = "fire"
                    mixer.Sound('resources/laser.wav').play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
    
    # Changes
    player.move()

    for enemy in enemies:
        enemy.move()
        if enemy.lose():
            enemies = []
            game_over = True
    
    if game_over == False:


        bullet.move()

        for i, enemy in enumerate(enemies):
            if enemy.is_hit(bullet):
                bullet.state = "ready"
                mixer.Sound('resources/explosion.wav').play()
                x = random.randint(0,800-64)
                y = random.randint(0,300-64)
                enemies.pop(i)

                player.score += 1
                bullet.x = player.x
                bullet.y = player.y
                bullet.change = 0

                if enemies == []:
                    round = create_enemies(round)

        # Set Items
        for enemy in enemies:
            enemy.enemy_set()
        if bullet.state == "fire":
            bullet.shoot()
    player.player_set()
    


    
    pygame.display.flip()