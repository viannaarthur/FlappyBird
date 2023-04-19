import pygame
import pygame.locals
import sys
import random
import os
import time

screen_width = 700
screen_heigth = 700
path = "C:/Users/arthu/Documents/ARTHUR/Scripts - Python/Flappy Bird/v2"
os.chdir(path)
pygame.init()

### IMPORTS ###
bird_image1 = pygame.image.load('bird3.png')
bird_image = pygame.transform.scale(bird_image1, (70,60))
pipe_image = pygame.transform.scale2x(pygame.image.load('pipe.png'))
background_image1 = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image1, (900,700))
wings_sound = pygame.mixer.Sound('wings_sound.wav')
score_sound = pygame.mixer.Sound('score_sound.wav')
die_sound = pygame.mixer.Sound('die_sound.wav')
text_font = pygame.font.SysFont('arial', 40, True, False)
loser1_font = pygame.font.SysFont('arial', 120, True, True)
loser2_font = pygame.font.SysFont('arial', 20, False, False)
loser1 = loser1_font.render('Loser!', True, (255,255,255), (0,0,0))
loser2 = loser2_font.render('Press [Space] to try again', True, (255,255,255),  (0,0,0))
init1_font = pygame.font.SysFont('arial', 30, False, False)
init2_font = pygame.font.SysFont('arial', 20, False, False)
init1 = init1_font.render('Select Level:', True, (255,255,255), (0,0,0))
init21 = init2_font.render('Press [1]: Noob', True, (255,255,255), (0,0,0))
init22 = init2_font.render('Press [2]: Gamer', True, (255,255,255), (0,0,0))
init23 = init2_font.render('Press [3]: Pro', True, (255,255,255), (0,0,0))
#################

class Bird:
    image = bird_image

    def __init__(self, x1, y1):
        self.x = x1
        self.y = y1
        self.y_ = y1
        self.up = 0
        self.time = 0
        self.image = bird_image
    
    def jump(self):
        self.up = -10
        self.time = 0
        self.y_ = self.y
    
    def move(self):
        self.time += 1
        desloc = 1.5*self.time**2 + self.up*self.time
        if desloc > 16:
            desloc = 16
        elif desloc < 0:
            desloc -=2
        self.y += desloc
    
    def draw(self, screen):
        global rect
        bird_center = self.image.get_rect(topleft=(self.x, self.y)).center
        self.bird_rect = self.image.get_rect(center=bird_center)
        screen.blit(self.image, self.bird_rect.topleft)
        rect = self.bird_rect

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    pipe_span = 200
    pipe_speed = 15

    def __init__(self, x2):
        self.x = x2
        self.y = 0
        self.top_pos = 0
        self.bottom_pos = 0
        self.bottom_pipe = pipe_image
        self.top_pipe = pygame.transform.flip(pipe_image, False, True)
        self.passed = False
        self.def_y()
    
    def def_y(self):
        self.y = random.randrange(50,500)
        self.top_pos = self.y - self.top_pipe.get_height()
        self.bottom_pos = self.y + self.pipe_span
    
    def move(self):
        self.x -= self.pipe_speed
    
    def draw(self, screen):
        screen.blit(self.top_pipe, (self.x, self.top_pos))
        screen.blit(self.bottom_pipe, (self.x, self.bottom_pos))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)
        dist_top = (self.x - bird.x, self.top_pos - round(bird.y))
        dist_bottom = (self.x - bird.x, self.bottom_pos - round(bird.y))
        over_top = bird_mask.overlap(top_mask, dist_top)
        over_bottom = bird_mask.overlap(bottom_mask, dist_bottom)
        if over_top or over_bottom:
            return True
        else:
            return False

def draw_screen(screen, bird, pipes, points):
    global counter
    screen.blit(background_image, (0,0))
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    counter = f'Score: {points}'
    text = text_font.render(counter, True, (0,0,0))
    screen.blit(text, (screen_width-text.get_width() -10, 10))
    pygame.display.update()

def main(FPS):
    global run
    bird = Bird(100,350)
    pipes = [Pipe(950)]
    screen = pygame.display.set_mode((screen_width, screen_heigth))
    points = 0
    clock = pygame.time.Clock()
    back_music = pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.15)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                wings_sound.play()
                bird.jump()            
        bird.move()
        new_pipe = False
        delete_pipe = []
        for pipe in pipes:
            if not pipe.passed and bird.x > pipe.x:
                pipe.passed = True
                new_pipe = True
            pipe.move()
            if pipe.collide(bird):
                run = False
                running = False
            if pipe.x + pipe.top_pipe.get_width() < 0:
                delete_pipe.append(pipe)
        if new_pipe:
            points += 1
            score_sound.play()
            FPS = FPS*1.01
            pipes.append(Pipe(720))
        for pipe in delete_pipe:
            pipes.remove(pipe)
        if bird.y > screen_heigth - 54:
            bird.y = screen_heigth - 54
        if bird.y < 0:
            bird.y = 0
        draw_screen(screen, bird, pipes, points)

play = True
while play:
    run = False
    while run == False:
        pygame.init()
        pygame.display.set_caption('Flappy Bird by pasteldeq')
        screen = pygame.display.set_mode((screen_width, screen_heigth))
        logo1 = os.path.join('logo.png')
        logo = pygame.image.load(logo1).convert()
        screen.fill((0,0,0))
        screen.blit(logo, (screen_width/2-340, screen_heigth/2-190))
        screen.blit(init1, (screen_width/2-90, screen_heigth/2+90))
        screen.blit(init21, (screen_width/2-78, screen_heigth/2+140))
        screen.blit(init22, (screen_width/2-85, screen_heigth/2+180))
        screen.blit(init23, (screen_width/2-68, screen_heigth/2+220))
        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    wait = False
                '''if pygame.key.get_pressed()[pygame.K_SPACE]:
                    run = True
                    pygame.display.update()
                    wait = False'''
                if pygame.key.get_pressed()[pygame.K_1]:
                    run = True
                    FPS = 20
                    pygame.display.update()
                    wait = False
                if pygame.key.get_pressed()[pygame.K_2]:
                    run = True
                    FPS = 30
                    pygame.display.update()
                    wait = False
                if pygame.key.get_pressed()[pygame.K_3]:
                    run = True
                    FPS = 40
                    pygame.display.update()
                    wait = False
        
    while run:
        if __name__ == '__main__':
            main(FPS)
    
    while run == False:
        text = text_font.render(counter, True, (255,255,255))
        screen.fill((0,0,0))
        screen.blit(loser1, (screen_width/2-175, screen_heigth/2-70))
        screen.blit(loser2, (screen_width/2-120, screen_heigth/2+55))
        screen.blit(text, (screen_width-200, 20))
        pygame.mixer.music.stop()
        pygame.display.flip()
        wait2 = True
        while wait2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    pygame.display.update()
                    wait2 = False
                    run = True