import asyncio
import sys
import pygame
from src.gameboard import Gameboard
from src.snake import Snake
from src.food import Food

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Global variables
done = False
started = False
score = 0
name = ""
delay = 0
size = (900, 600)
namelist = [""]
scorelist = ["0"]

# Initialize pygame
pygame.init()
pygame.mixer.init()

titlescreen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game - By Luis Tallavo")

# Load audio - use OGG for web, WAV for desktop
if sys.platform == "emscripten":
    pygame.mixer.music.load('assets/Snakesong.ogg')
else:
    try:
        pygame.mixer.music.load('assets/Snakesong.ogg')
    except:
        pygame.mixer.music.load('assets/Snakesong.wav')
pygame.mixer.music.play(-1)

gamescreen = Gameboard(WHITE, 20)
playersnake = Snake()
realfood = Food()

scorefont = pygame.font.Font('freesansbold.ttf', 20)
HSfont = pygame.font.Font('freesansbold.ttf', 20)

# Load high scores
try:
    with open("Highscores.txt", "r") as HSfile:
        namelist[0] = HSfile.readline().rstrip('\n')
        scorelist[0] = HSfile.readline().rstrip('\n')
except:
    namelist = [""]
    scorelist = ["0"]

screen = None


def drawscreen():
    screen.fill(BLACK)
    gamescreen.draw(screen)
    playersnake.draw(screen)
    realfood.draw(screen)
    scoretext = scorefont.render("Score: " + str(score), 1, WHITE)
    screen.blit(scoretext, (570, 75))
    for i in range(1):
        hsnametext = HSfont.render(str(namelist[i]), 1, WHITE)
        hsscoretext = HSfont.render(str(scorelist[i]), 1, WHITE)
        screen.blit(hsnametext, (710, i * 25 + 125))
        screen.blit(hsscoretext, (800, i * 25 + 125))
    pygame.draw.rect(screen, WHITE, [700, 100, 150, 200], 1)
    highscoretext = HSfont.render("High Scores", 1, WHITE)
    screen.blit(highscoretext, (710, 75))
    pygame.display.flip()


def KeyCheck(event):
    global playersnake
    if playersnake.xspeed != 0 and playersnake.yspeed == 0:
        if event.key == pygame.K_DOWN:
            playersnake.yspeed = 1
            playersnake.xspeed = 0
        elif event.key == pygame.K_UP:
            playersnake.yspeed = -1
            playersnake.xspeed = 0
    if playersnake.yspeed != 0 and playersnake.xspeed == 0:
        if event.key == pygame.K_LEFT:
            playersnake.xspeed = -1
            playersnake.yspeed = 0
        elif event.key == pygame.K_RIGHT:
            playersnake.xspeed = 1
            playersnake.yspeed = 0


def checkHighScores():
    global scorelist, namelist
    newhighscore = False
    tempnamelist = [""]
    tempscorelist = [0]
    for i in range(1):
        try:
            current_score = int(scorelist[i]) if scorelist[i] else 0
        except:
            current_score = 0
        if score > current_score and not newhighscore:
            newhighscore = True
            tempscorelist[i] = score
            tempnamelist[i] = name
        elif newhighscore:
            tempscorelist[i] = scorelist[i - 1]
            tempnamelist[i] = namelist[i - 1]
        else:
            tempscorelist[i] = scorelist[i]
            tempnamelist[i] = namelist[i]

    for i in range(1):
        scorelist[i] = tempscorelist[i]
        namelist[i] = tempnamelist[i]

    # Only write high scores on desktop (not available in web)
    if sys.platform != "emscripten":
        try:
            with open("Highscores.txt", "w") as HSfile:
                for i in range(1):
                    HSfile.write(str(namelist[i]) + '\n')
                for i in range(1):
                    HSfile.write(str(scorelist[i]) + '\n')
        except:
            pass


async def main():
    global done, started, score, name, delay, screen
    global gamescreen, playersnake, realfood

    # Title screen loop
    while not started:
        startpic = pygame.image.load("assets/snakescreen.png")
        enterednametext = scorefont.render("Please Type in Your Name", 1, WHITE)
        nametext = scorefont.render(name, 1, WHITE)
        titlescreen.blit(enterednametext, (500, 200))
        titlescreen.blit(nametext, (500, 250))
        pygame.display.flip()
        titlescreen.blit(startpic, (-75, -20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                started = True
            if event.type == pygame.KEYDOWN:
                if event.key >= 33 and event.key <= 126 and len(name) < 10:
                    name = name + chr(event.key)
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                if event.key == pygame.K_SPACE:
                    if name == "":
                        name = "Player1"
                    started = True

        await asyncio.sleep(0)

    screen = pygame.display.set_mode(size)

    # Main game loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                KeyCheck(event)

        delay += 1
        if delay >= 10:
            delay = 0
            playersnake.updatePosition()
            if playersnake.CanSnakeMove():
                playersnake.movesnake()

        if playersnake.eatfood(realfood):
            realfood = Food()
            playersnake.total += 1
            score += 10 * playersnake.total
            playersnake.fullsnake.append(playersnake.tail[-playersnake.total])

        if gamescreen.checkDeath(playersnake):
            gamescreen = Gameboard(WHITE, 20)
            playersnake = Snake()
            realfood = Food()
            checkHighScores()
            score = 0

        drawscreen()

        await asyncio.sleep(0)


# Entry point
asyncio.run(main())
