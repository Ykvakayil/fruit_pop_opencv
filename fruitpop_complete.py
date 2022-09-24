# Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
from pygame import mixer
def game():
    # Initialize
    pygame.init()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balloon Pop")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # width
    cap.set(4, 720)  # height

    # Images

    background = pygame.image.load("../resources/images/fruitninja.jpg").convert()
    fruit1 = pygame.image.load('../resources/images/banana.png').convert_alpha()
    rect_fruit1 = fruit1.get_rect()
    rect_fruit1.x, rect_fruit1.y = 350, 1000

    fruit2 = pygame.image.load('../resources/images/peach.png').convert_alpha()
    rect_fruit2 = fruit2.get_rect()
    rect_fruit2.x, rect_fruit2.y = 590, 1350

    fruit3 = pygame.image.load('../resources/images/watermelon.png').convert_alpha()
    rect_fruit3 = fruit3.get_rect()
    rect_fruit3.x, rect_fruit3.y = 750, 1700

    fruit4 = pygame.image.load('../resources/images/apple.png').convert_alpha()
    rect_fruit4 = fruit4.get_rect()
    rect_fruit4.x, rect_fruit4.y = 1000, 1900

    bomb = pygame.image.load("../resources/images/boom.png").convert_alpha()
    rect_bomb = bomb.get_rect()
    rect_bomb.x, rect_bomb.y = 780, 2100

    over = pygame.image.load("../resources/images/game-over.png").convert_alpha()

    mixer.music.load("../resources/images/sounds/start.mp3")
    mixer.music.play()

    # Variables
    speed = 15
    score = 0
    startTime = time.time()
    totalTime = 60

    # Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)


    def reset_fruit1():
        rect_fruit1.x = random.randint(100, img.shape[1] - 100)
        rect_fruit1.y = img.shape[0] + 50


    def reset_fruit2():
        rect_fruit2.x = random.randint(100, img.shape[1] - 200)
        rect_fruit2.y = img.shape[0] + 150


    def reset_fruit3():
        rect_fruit3.x = random.randint(100, img.shape[1] - 300)
        rect_fruit3.y = img.shape[0] + 250


    def reset_fruit4():
        rect_fruit4.x = random.randint(100, img.shape[1] - 400)
        rect_fruit4.y = img.shape[0] + 350

    def reset_bomb():
        rect_bomb.x = random.randint(100, img.shape[1] - 500)
        rect_bomb.y = img.shape[0] + 255

    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        # Apply Logic
        timeRemain = int(totalTime - (time.time()-startTime))
        if timeRemain < 0:
            window.fill((255, 255, 255))

            font = pygame.font.Font('./resources/BungeeSpice-Regular.ttf', 50)
            textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
            textTime = font.render(f'Time UP', True, (50, 50, 255))
            window.blit(textScore, (450, 350))
            window.blit(textTime, (530, 275))

        else:
            # OpenCV
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)

            rect_fruit1.y -= speed  # Move the balloon up
            rect_fruit2.y -= speed
            rect_fruit3.y -= speed
            rect_fruit4.y -= speed
            rect_bomb.y -= speed
            # check if balloon has reached the top without pop
            if rect_fruit1.y < 0:
                reset_fruit1()
            if rect_fruit2.y < 0:
                reset_fruit2()
            if rect_fruit3.y < 0:
                reset_fruit3()
            if rect_fruit4.y < 0:
                reset_fruit4()
            if rect_bomb.y < 0:
                reset_bomb()

            if hands:
                hand = hands[0]
                x, y = hand['lmList'][8][0:2]
                collide_sound = mixer.Sound("../resources/images/sounds/splatter.mp3")
                if rect_fruit1.collidepoint(x, y):
                    collide_sound.play()
                    reset_fruit1()
                    score += 10
                    speed += 1
                if rect_fruit2.collidepoint(x, y):
                    collide_sound.play()
                    reset_fruit2()
                    score += 10
                    speed += 1
                if rect_fruit3.collidepoint(x, y):
                    collide_sound.play()
                    reset_fruit3()
                    score += 20
                    speed += 1
                if rect_fruit4.collidepoint(x, y):
                    collide_sound.play()
                    reset_fruit4()
                    score += 20
                    speed += 1
                if rect_bomb.collidepoint(x, y):
                    bomb_sound = mixer.Sound("../resources/images/sounds/boom.mp3")
                    bomb_sound.play()
                    window.blit(background, (0, 0))
                    window.blit(over, (375, 250))
                    font = pygame.font.Font('../resources/BungeeSpice-Regular.ttf', 50)
                    textScore = font.render(f'Score: {score}', True, (252, 163, 0))
                    textTime = font.render(f'Time: {timeRemain}', True, (252, 163, 255))
                    window.blit(textScore, (190, 495))
                    window.blit(textTime, (800, 495))
                    pygame.display.update()
                    time.sleep(15)
                    pygame.quit()



            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)

            window.blit(frame, (0, 0))
            window.blit(fruit1, rect_fruit1)
            window.blit(fruit2, rect_fruit2)
            window.blit(fruit3, rect_fruit3)
            window.blit(fruit4, rect_fruit4)
            window.blit(bomb, rect_bomb)

            font = pygame.font.Font('../resources/BungeeSpice-Regular.ttf', 50)
            textScore = font.render(f'Score: {score}', True, (252, 163, 0))
            textTime = font.render(f'Time Rem: {timeRemain}', True, (255, 115, 0))
            window.blit(textScore, (10, 10))
            window.blit(textTime, (800, 10))

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)