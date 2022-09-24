import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
from pygame import mixer
import fruitpop_complete

pygame.init()

width, height = 1280, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fruit Ninja")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

fps = 60
clock = pygame.time.Clock()

start = True

score = 0
startTime = time.time()
totalTime = 60

background = pygame.image.load("../resources/images/fruitninja.jpg").convert()
fruit1 = pygame.image.load("../resources/apple.png").convert_alpha()
fruit2 = pygame.image.load("../resources/images/banana.png").convert_alpha()
fruit3 = pygame.image.load("../resources/images/watermelon.png").convert_alpha()
fruit4 = pygame.image.load("../resources/images/peach.png").convert_alpha()
over = pygame.image.load("../resources/images/game-over.png").convert_alpha()
fruit = pygame.image.load("../resources/images/fruit.png").convert_alpha()
ninja = pygame.image.load("../resources/images/ninja.png").convert_alpha()
newgame = pygame.image.load("../resources/images/new-game.png").convert_alpha()
rect_newgame = newgame.get_rect()
rect_newgame.x, rect_newgame.y = 500, 200
detector = HandDetector(detectionCon=0.8, maxHands=1)

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()


    timeRemain = int(totalTime - (time.time() - startTime))
    if timeRemain < 0:
        window.fill((255, 255, 255))
        '''
        font = pygame.font.Font('./resources/BungeeSpice-Regular.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time UP', True, (50, 50, 255))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))'''

    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8][0:2]
            if rect_newgame.collidepoint(x, y):
                start_button_sound = mixer.Sound("../resources/images/sounds/missed.mp3")
                start_button_sound.play()
                fruitpop_complete.game()


        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)

        window.blit(frame, (0, 0))
        window.blit(fruit, (100, 100))
        window.blit(ninja, (200, 200))
        window.blit(newgame, (500, 150))
        window.blit(fruit1, (100, 500))
        window.blit(fruit2, (100, 600))
        window.blit(fruit3, (750, 500))
        window.blit(fruit4, (750, 600))
        font = pygame.font.Font('../resources/BungeeSpice-Regular.ttf', 50)
        fruit1text = font.render(' - Points: 10', True, (255, 115, 0))
        fruit2text = font.render(' - Points: 10', True, (255, 115, 0))
        fruit3text = font.render(' - Points: 20', True, (255, 115, 0))
        fruit4text = font.render(' - Points: 20', True, (255, 115, 0))
        window.blit(fruit1text, (250, 500))
        window.blit(fruit2text, (250, 600))
        window.blit(fruit3text, (880, 500))
        window.blit(fruit4text, (880, 600))
    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)
