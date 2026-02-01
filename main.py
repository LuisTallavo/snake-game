import asyncio
import sys
import pygame
from src.gameboard import Gameboard
from src.snake import Snake
from src.food import Food

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

MOVE_INTERVAL = 100  # milliseconds between moves

# Global variables
done = False
started = False
score = 0
name = ""
size = (900, 600)
namelist = []
scorelist = []
last_move_time = 0
show_quit_message = False
MAX_HIGH_SCORES = 5

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
buttonfont = pygame.font.Font('freesansbold.ttf', 16)

# Load high scores (format: name,score per line)
def load_high_scores():
    global namelist, scorelist
    namelist = []
    scorelist = []
    try:
        with open("Highscores.txt", "r") as HSfile:
            for line in HSfile:
                line = line.rstrip('\n')
                if ',' in line:
                    parts = line.split(',', 1)
                    namelist.append(parts[0])
                    scorelist.append(parts[1])
    except:
        pass

load_high_scores()

screen = None

home_button_rect = pygame.Rect(700, 320, 65, 30)
quit_button_rect = pygame.Rect(700, 360, 55, 30)
reset_button_rect = pygame.Rect(770, 320, 75, 30)


def drawscreen():
    global show_quit_message

    screen.fill(BLACK)

    # If quit message is showing, display it and return
    if show_quit_message:
        quit_msg = scorefont.render("Game Over!", 1, WHITE)
        close_msg = scorefont.render("You can close this tab now.", 1, WHITE)
        screen.blit(quit_msg, (350, 250))
        screen.blit(close_msg, (300, 300))
        pygame.display.flip()
        return

    gamescreen.draw(screen)
    playersnake.draw(screen)
    realfood.draw(screen)
    scoretext = scorefont.render("Score: " + str(score), 1, WHITE)
    screen.blit(scoretext, (570, 75))

    # High scores display
    pygame.draw.rect(screen, WHITE, [700, 100, 150, 200], 1)
    highscoretext = HSfont.render("High Scores", 1, WHITE)
    screen.blit(highscoretext, (710, 75))

    # Display high score entries
    for i in range(min(len(namelist), MAX_HIGH_SCORES)):
        if namelist[i]:
            hsnametext = HSfont.render(str(namelist[i])[:8], 1, WHITE)
            hsscoretext = HSfont.render(str(scorelist[i]), 1, WHITE)
            screen.blit(hsnametext, (710, i * 25 + 125))
            screen.blit(hsscoretext, (800, i * 25 + 125))

    # Draw Home button
    pygame.draw.rect(screen, GRAY, home_button_rect)
    pygame.draw.rect(screen, WHITE, home_button_rect, 2)
    home_text = buttonfont.render("Home", 1, WHITE)
    screen.blit(home_text, (home_button_rect.x + 10, home_button_rect.y + 7))

    # Draw Quit button
    pygame.draw.rect(screen, GRAY, quit_button_rect)
    pygame.draw.rect(screen, WHITE, quit_button_rect, 2)
    quit_text = buttonfont.render("Quit", 1, WHITE)
    screen.blit(quit_text, (quit_button_rect.x + 10, quit_button_rect.y + 7))

    # Draw Reset button
    pygame.draw.rect(screen, GRAY, reset_button_rect)
    pygame.draw.rect(screen, WHITE, reset_button_rect, 2)
    reset_text = buttonfont.render("Reset", 1, WHITE)
    screen.blit(reset_text, (reset_button_rect.x + 10, reset_button_rect.y + 7))

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


def save_high_scores():
    if sys.platform != "emscripten":
        try:
            with open("Highscores.txt", "w") as HSfile:
                for i in range(len(namelist)):
                    HSfile.write(f"{namelist[i]},{scorelist[i]}\n")
        except:
            pass

def reset_high_scores():
    global namelist, scorelist
    namelist = []
    scorelist = []
    save_high_scores()

def checkHighScores():
    global scorelist, namelist

    if score == 0:
        return

    # Find the position to insert the new score
    insert_pos = len(namelist)
    for i in range(len(scorelist)):
        try:
            if score > int(scorelist[i]):
                insert_pos = i
                break
        except ValueError:
            insert_pos = i
            break

    # Insert the new score at the correct position
    namelist.insert(insert_pos, name)
    scorelist.insert(insert_pos, str(score))

    # Keep only the top MAX_HIGH_SCORES
    namelist = namelist[:MAX_HIGH_SCORES]
    scorelist = scorelist[:MAX_HIGH_SCORES]

    save_high_scores()

def reset_game():
    """Reset the game state for a new game or returning home."""
    global gamescreen, playersnake, realfood, score
    gamescreen = Gameboard(WHITE, 20)
    playersnake = Snake()
    realfood = Food()
    score = 0


async def title_screen():
    """Handle the title screen and return when player is ready to start."""
    global done, name
    
    startpic = pygame.image.load("assets/snakescreen.png")
    
    while True:
        titlescreen.blit(startpic, (-75, -20))
        enterednametext = scorefont.render("Please Type in Your Name", 1, WHITE)
        nametext = scorefont.render(name, 1, WHITE)
        instructiontext = scorefont.render("Press SPACE to start", 1, WHITE)
        titlescreen.blit(enterednametext, (500, 200))
        titlescreen.blit(nametext, (500, 250))
        titlescreen.blit(instructiontext, (500, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return False
            if event.type == pygame.KEYDOWN:
                if event.key >= 33 and event.key <= 126 and len(name) < 10:
                    name = name + chr(event.key)
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                if event.key == pygame.K_SPACE:
                    if name == "":
                        name = "Player1"
                    return True

        await asyncio.sleep(0)


async def game_loop():
    """Main game loop. Returns 'home' to go back to title, 'quit' to exit."""
    global done, score, last_move_time, show_quit_message
    global gamescreen, playersnake, realfood, screen

    clock = pygame.time.Clock()
    last_move_time = pygame.time.get_ticks()

    while not done:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if not show_quit_message:
                    KeyCheck(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if show_quit_message:
                    continue
                if home_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    return 'home'
                if quit_button_rect.collidepoint(mouse_pos):
                    if sys.platform == "emscripten":
                        show_quit_message = True
                        pygame.mixer.music.stop()
                    else:
                        return 'quit'
                if reset_button_rect.collidepoint(mouse_pos):
                    reset_high_scores()

        # Skip game logic if showing quit message
        if show_quit_message:
            drawscreen()
            await asyncio.sleep(0)
            continue

        # Time-based movement for smooth animation
        if current_time - last_move_time >= MOVE_INTERVAL:
            last_move_time = current_time
            playersnake.updatePosition()
            if playersnake.CanSnakeMove():
                playersnake.movesnake()

        if playersnake.eatfood(realfood):
            realfood = Food()
            playersnake.total += 1
            score += 10 * playersnake.total
            playersnake.fullsnake.append(playersnake.tail[-playersnake.total])

        if gamescreen.checkDeath(playersnake):
            checkHighScores()
            reset_game()

        drawscreen()

        await asyncio.sleep(0)

    return 'quit'


async def main():
    global done, screen
    
    while not done:
        # Show title screen
        should_start = await title_screen()
        if not should_start:
            break
        
        # Setup game screen
        screen = pygame.display.set_mode(size)
        reset_game()
        
        # Run game loop
        result = await game_loop()
        
        if result == 'quit':
            break
        # If result == 'home', loop continues back to title screen

# Entry point
asyncio.run(main())
