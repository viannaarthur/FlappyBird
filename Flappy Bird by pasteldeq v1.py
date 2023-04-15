import pygame
import pygame.locals
import sys
import random
import os
import time

play = True
a = 0
b = 0
path = "C:/Users/arthu/Documents/ARTHUR/Scripts - Python/Flappy Bird/v1"
os.chdir(path)
run = False

while play:
    pygame.init()
    width = 900
    height = 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Flappy Bird by pasteldeq')
    logo1 = os.path.join('logo.png')
    logo = pygame.image.load(logo1).convert()
    bird = pygame.image.load('bird3.png').convert_alpha()
    #bird_rect = bird.get_rect()
    x1 = 10
    y1 = height/2 - 25
    x2 = width
    x3 = width + 450
    y2 = random.randint(20, 480)
    if y2 >= height-300:
        y3 = random.randint(y2-200, 480)
    elif y2 <= 300:
        y3 = random.randint(20, y2+200)
    else:
        y3 = random.randint(y2-200, y2+200)
    delta_y = 0.2
    delta_x = 0.5
    up = 30
    count = 0
    init_font = pygame.font.SysFont('arial', 20, False, False)
    init = init_font.render('Press [Space]', True, (255,255,255), (0,0,0))
    text_font = pygame.font.SysFont('arial', 40, True, False)
    loser1_font = pygame.font.SysFont('arial', 120, True, True)
    loser2_font = pygame.font.SysFont('arial', 20, False, False)
    loser1 = loser1_font.render('Loser!', True, (255,255,255), (0,0,0))
    loser2 = loser2_font.render('Press [Space] to try again', True, (255,255,255),  (0,0,0))
    back_music = pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.15)
    wings_sound = pygame.mixer.Sound('wings_sound.wav')
    score_sound = pygame.mixer.Sound('score_sound.wav')
    die_sound = pygame.mixer.Sound('die_sound.wav')

    while run == False:
        screen.fill((0,0,0))
        screen.blit(logo, (width/2-340, height/2-190))
        screen.blit(init, (width/2-70, height/2+100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                run = True
                pygame.display.update()

    while run:
        counter = f'Score: {count}'
        text = text_font.render(counter, True, (255,255,255))
        screen.fill((173,216,230))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                y1 = y1-up
                wings_sound.play()
        if y1 >= height-50:
            y1 = height-50
        if y1 < 0:
            y1 = 0
        y1 = y1+delta_y
        pipe1 = pygame.draw.rect(screen, (0,255,0), (x2,y2-height,40,height))
        pipe2 = pygame.draw.rect(screen, (0,255,0), (x2,y2+160,40,height))
        pipe3 = pygame.draw.rect(screen, (0,255,0), (x3,y3-height,40,height))
        pipe4 = pygame.draw.rect(screen, (0,255,0), (x3,y3+160,40,height))
        bird2 = screen.blit(bird, (x1, y1))
        x2 = x2 - delta_x
        x3 = x3 - delta_x
        if x2 <= 0:
            x2 = width
            if y3 >= height-200:
                y2 = random.randint(y3-200, 500)
            elif y3 <= height+200:
                y2 = random.randint(50, y3+200)
            else:
                y2 = random.randint(y3-200, y3+200)
            count = count +1
            score_sound.play()
        if x3 <= 0:
            x3 = width
            if y2 >= height-200:
                y3 = random.randint(y2-200, 500)
            elif y2 <= height+200:
                y3 = random.randint(50, y2+200)
            else:
                y3 = random.randint(y2-200, y2+200)
            count = count +1
            score_sound.play()
        if bird2.colliderect(pipe1) or bird2.colliderect(pipe2) or bird2.colliderect(pipe3) or bird2.colliderect(pipe4):
            run = False
            break
        screen.blit(text, (width-200, 20))
        delta_y = delta_y*1.00004
        delta_x = delta_x*1.00003
        up = up*1.00003
        pygame.display.update()
    
    while run == False:
        screen.fill((0,0,0))
        screen.blit(loser1, (width/2-175, height/2-70))
        screen.blit(loser2, (width/2-120, height/2+55))
        screen.blit(text, (width-200, 20))
        pygame.mixer.music.stop()
        die_sound.play()
        delta_y = 0
        delta_x = 0
        up = 0
        run = False
        pygame.display.flip()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    run = True
                    pygame.display.update()
                    wait = False