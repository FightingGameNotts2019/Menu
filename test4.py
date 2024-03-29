# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:26:46 2019

@author: nabid
"""

import pygame
#import gameScreen
import os

# Still not fixed these, leave them for now.
WIDTH = 1600
HEIGHT = 800
PLAYER_HEIGHT = 20
PLAYER_WIDTH = 59
Level_select = 1
LVL_1_GROUND = (HEIGHT - 130)
FPS = 40
ANIMATION = 4  # for when they move
clock = pygame.time.Clock()  # sets internal clock for the game
# Player life
LIFE = 200
TAKE_LIFE = 20
# Actions, these are good I found and because we have the FPS they should be consistent
GRAVITY = 20
MOVING_SPEED = 20
# Not used yet

JUMP_HEIGHT = 360  # This is actually double
PLAYER1_X = 500
PLAYER1_Y = 540

HIT_TIME = 100


class Platform:
    # Defines size, position and colour of platform objects
    def __init__(self, size_x, size_y, pos_x, pos_y, colour):
        self.surface = pygame.Surface((size_x, size_y))
        self.rect = self.surface.get_rect(midtop=(pos_x, pos_y))
        self.surface.fill(colour)

        # draws the platform on the game screen
    def draw(self):
        screen.blit(self.surface, self.rect)


class Player:
    # Probably need to add separate colours for each player, but then aagin we have the sprites?
    def __init__(self, x, y):
        # These are not used but DO NO CHANGE.
        self.x = x
        self.y = y
        # the life rectangles for each player
        self.life = pygame.Rect(100, 100, LIFE, 30)
        self.life2 = pygame.Rect(1300, 100, LIFE, 30)
        # PLayer hitboxes
        self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
        self.hitbox2 = pygame.Rect(self.x + 400, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
        # Used in the jump function.
        self.jump1 = False
        self.jump2 = False
        self.jumpCount = JUMP_HEIGHT
        self.jumpCount2 = JUMP_HEIGHT
        # Hitting things
        self.hit = False
        self.hitCount = HIT_TIME
        self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
        self.dir = 1

        self.hit2 = False
        self.hitCount2 = HIT_TIME
        self.arm2 = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
        self.dir2 = -1
        # Updates the player, called after every action.

    def show(self, colour, screen,STAGE):
       # global STAGE

        STAGE.Level_load(screen)
        pygame.draw.rect(screen, colour, self.hitbox)
        pygame.draw.rect(screen, colour, self.hitbox2)
        pygame.draw.rect(screen, colour, self.life)
        pygame.draw.rect(screen, colour, self.life2)
        if self.hit:
            pygame.draw.rect(screen, pygame.Color("green"), self.arm)
        if self.hit2:
            pygame.draw.rect(screen, pygame.Color("green"), self.arm2)

        # Draws platforms
        #for i in platforms:
         #   i.draw()

    # Always falling unless touching the stage or jumping. Need to mess around with the accelation.
    #def falling(self):
     ##   global plColor
       # global STAGE

        #if not self.hitbox.colliderect(STAGE) and not self.jump1:
         #   self.hitbox.move_ip(0, GRAVITY)
          #  self.show(plColor, screen)
       # if not self.hitbox2.colliderect(STAGE) and not self.jump2:
        #    self.hitbox2.move_ip(0, GRAVITY)
         #   self.show(plColor, screen)

        # Resets a player if he falls off the stage and takes a life

    def reset(self,STAGE):
        global plColor

        if self.hitbox.y >= 940:
            self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
            self.getHit(1)
            self.show(plColor, screen,STAGE)
        if self.hitbox2.y >= 940:
            self.hitbox2 = pygame.Rect(self.x + 400, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
            self.getHit(2)
            self.show(plColor, screen,STAGE)

        # Static move, can mess around with acceleration later

    def move(self,STAGE):
        global plColor

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)
            self.show(plColor, screen,STAGE)
            self.dir = -1
        if keys[pygame.K_d]:
            self.hitbox.move_ip(MOVING_SPEED, 0)
            self.show(plColor, screen,STAGE)
            self.dir = 1

        if keys[pygame.K_LEFT]:
            self.hitbox2.move_ip(-MOVING_SPEED, 0)
            self.show(plColor, screen,STAGE)
            self.dir2 = -1
        if keys[pygame.K_RIGHT]:
            self.hitbox2.move_ip(MOVING_SPEED, 0)
            self.show(plColor, screen,STAGE)
            self.dir2 = 1

        # Static jump, can mess around with equation later. We can try double jump later, shouldnt be too bad.

    def jump(self,STAGE):

        global plColor
        if self.jump1:
            if self.jumpCount >= JUMP_HEIGHT / 2:
                self.hitbox.move_ip(0, -GRAVITY)
                self.jumpCount -= GRAVITY
                self.show(plColor, screen,STAGE)
            elif self.jumpCount >= 0:
                self.hitbox.move_ip(0, GRAVITY)
                self.jumpCount -= GRAVITY
                self.show(plColor, screen,STAGE)
            else:
                self.jump1 = False
                self.jumpCount = JUMP_HEIGHT

        if self.jump2:
            if self.jumpCount2 >= JUMP_HEIGHT / 2:
                self.hitbox2.move_ip(0, -GRAVITY)
                self.jumpCount2 -= GRAVITY
                self.show(plColor, screen,STAGE)
            elif self.jumpCount2 >= 0:
                self.hitbox2.move_ip(0, GRAVITY)
                self.jumpCount2 -= GRAVITY
                self.show(plColor, screen,STAGE)
            else:
                self.jump2 = False
                self.jumpCount2 = JUMP_HEIGHT

    # Only hits in one direction. Potential solutions: implement direction? or implement 2 buttons to hit for each direction.
    # Also arm isnt attached, it sort of drags behind, not sure how much of a problem it is.
    # Also no actual collsion yet.
    def hitting(self,STAGE):
        global screen

        if self.hit:
            if self.hitCount >= 0:
                if self.dir == 1:
                    self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
                else:
                    self.arm = pygame.Rect(self.hitbox.x - 15, self.hitbox.y, 15, 5)
                # pygame.draw.rect(screen,pygame.Color('green') , arm)
                self.hitCount -= 5
                self.show(plColor, screen,STAGE)
            else:
                self.hit = False
                self.hitCount = HIT_TIME
                self.show(plColor, screen,STAGE)

        if self.hit2:
            if self.hitCount2 >= 0:
                if self.dir2 == 1:
                    self.arm2 = pygame.Rect(self.hitbox2.x + 20, self.hitbox2.y, 15, 5)
                else:
                    self.arm2 = pygame.Rect(self.hitbox2.x - 15, self.hitbox2.y, 15, 5)
                # pygame.draw.rect(screen,pygame.Color('green') , arm)
                self.hitCount2 -= 5
                self.show(plColor, screen,STAGE)
            else:
                self.hit2 = False
                self.hitCount2 = HIT_TIME
                self.show(plColor, screen,STAGE)

    # Gets called whenever the player gets hit and reduces that players life.
    def getHit(self, player,STAGE):
        if player == 1:
            self.life.inflate_ip(-TAKE_LIFE, 0)
            self.show(plColor, screen,STAGE)
        if player == 2:
            self.life2.inflate_ip(-TAKE_LIFE, 0)
            self.show(plColor, screen,STAGE)

    # For this need a timer and a way to make the player flash?
    def invincible(self):
        pass

    # Need to figure out how to do a timer, pygame.time.get_ticks() might work?


# =============================================================================
#     def stop(self):
#         while True:
#             clocka = pygame.time.Clock()
#             timer = 2
#             dt = 0
#             timer -= dt
#             if timer <= 0:
#                 break
#
#             dt = clocka.tick(60)/100
# =============================================================================

class Stage:

    def __init__(self, level_select):
        self.level_select = level_select

    SKY = (102, 178, 255)
    GREY = (38, 38, 38)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)  # Designated ALPHA colour, if you need something to exist but not be seen make it this colour
    bgColor = pygame.Color("white")
    fgColor = pygame.Color("black")
    plColor = SKY

    def Level_load(self,screen):
        if self.level_select == 1:
            background = pygame.image.load(os.path.join('images', 'background1.png')).convert()
            background_box = screen.get_rect()  # Fits background to screen
            screen.blit(background, background_box)  # This makes the background load up
            platforms = []  # list for platforms to go in
            platforms.append(Platform(WIDTH, 1, WIDTH // 2, LVL_1_GROUND, self.GREEN))  # These are the platforms for level 1
            platforms.append(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, self.BLACK))
            platforms.append(Platform(200, 20, WIDTH // 4, HEIGHT // 2, self.BLACK))
            platforms.append(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, self.BLACK))
            p_rects = [i.rect for i in platforms]
        if self.level_select == 2:
            background = pygame.image.load(os.path.join('images', 'background2.png')).convert()
            background_box = screen.get_rect()  # Fits background to screen
            screen.blit(background, background_box)  # This makes the background load up
            platforms = []  # list for platforms to go in
            platforms.append(Platform(WIDTH, 1, WIDTH // 2, LVL_1_GROUND, self.GREEN))  # These are the platforms for level 1
            platforms.append(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, self.BLACK))
            platforms.append(Platform(200, 20, WIDTH // 4, HEIGHT // 2, self.BLACK))
            platforms.append(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, self.BLACK))
            p_rects = [i.rect for i in platforms]
        if self.level_select == 3:
            background = pygame.image.load(os.path.join('images', 'background3.png')).convert()
            background_box = screen.get_rect()  # Fits background to screen
            screen.blit(background, background_box)  # This makes the background load up
            platforms = []  # list for platforms to go in
            platforms.append(Platform(WIDTH, 1, WIDTH // 2, LVL_1_GROUND, self.GREEN))  # These are the platforms for level 1
            platforms.append(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, self.BLACK))
            platforms.append(Platform(200, 20, WIDTH // 4, HEIGHT // 2, self.BLACK))
            platforms.append(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, self.BLACK))
            p_rects = [i.rect for i in platforms]




   
def main(level):
    STAGE = Stage(level)
    display_width = 1600
    display_height = 800
    screen = pygame.display.set_mode((display_width,display_height))
    
     
    
    # Colours, will change these later
    fgColor = pygame.Color("black")
    plColor = pygame.Color('red')
    # filling the background (255,255,255) is just white
    screen.fill((255, 255, 255))
    
    
    SKY = (102, 178, 255)
    GREY = (38, 38, 38)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)  # Designated ALPHA colour, if you need something to exist but not be seen make it this colour
    bgColor = pygame.Color("white")
    fgColor = pygame.Color("black")
    plColor = SKY
    #STAGE = Stage(level)
    # Initialise our players
    PLAYER = Player(PLAYER1_X, PLAYER1_Y)
    PLAYER.show(plColor, screen,STAGE)
    
    while True:
        # all our events, might be worth putting into a method later, leave for now.
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                PLAYER.jump1 = True
            if e.key == pygame.K_UP:
                PLAYER.jump2 = True
            if e.key == pygame.K_s:
                PLAYER.hit = True
            if e.key == pygame.K_DOWN:
                PLAYER.hit2 = True
    
        clock.tick(FPS)
        #Level_select = 1
        # All the actions
        PLAYER.move(STAGE)
        PLAYER.jump(STAGE)
        #PLAYER.falling()
        PLAYER.hitting(STAGE)
        PLAYER.reset(STAGE)
        # Update the display
        pygame.display.flip()
    
    pygame.quit()