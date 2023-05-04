import pygame
import random

# Set up the game window
canvas_width = 800
canvas_height = 400
pygame.init()
win = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Egg Catcher")
clock = pygame.time.Clock()

# Set up game variables
color_cycle = iter([(173, 216, 230), (255, 182, 193), (255, 255, 224), (144, 238, 144), (255, 0, 0), (0, 0, 255), (0, 128, 0)])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty_factor = 0.95
catcher_color = (0, 0, 255)
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width/2 - catcher_width/2
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_y2 = catcher_start_y + catcher_height
score = 0
lives_remaining = 3

# Set up game font
game_font = pygame.font.SysFont('FixedFont', 18)

# Create catcher
catcher_rect = pygame.draw.arc(win, catcher_color, (catcher_start_x, catcher_start_y, catcher_width, catcher_height), 3.49, 6.08, 3)

# Create score and lives text
score_text = game_font.render("Score: " + str(score), True, (0, 0, 139))
lives_text = game_font.render("Lives: " + str(lives_remaining), True, (0, 0, 139))

# Create eggs list
eggs = []

# Define game functions
def create_egg():
    x = random.randint(10, 740)
    y = 40
    new_egg = pygame.draw.ellipse(win, next(color_cycle), (x, y, egg_width, egg_height))
    eggs.append(new_egg)
    pygame.time.set_timer(pygame.USEREVENT, egg_interval)

def move_eggs():
    global lives_remaining
    for egg in eggs:
        egg.move_ip(0, 10)
        if egg.bottom > canvas_height:
            eggs.remove(egg)
            lose_a_life()
            if lives_remaining == 0:
                game_over()
    pygame.time.set_timer(pygame.USEREVENT+1, egg_speed)

def lose_a_life():
    global lives_remaining, lives_text
    lives_remaining -= 1
    lives_text = game_font.render("Lives: " + str(lives_remaining), True, (0, 0, 139))

def check_catch():
    global score, egg_speed, egg_interval
    for egg in eggs:
        if catcher_rect.colliderect(egg):
            eggs.remove(egg)
            increase_score(egg_score)
            pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT+2, 100)

def increase_score(points):
    global score, score_text, egg_speed, egg_interval
    score += points
    score_text = game_font.render("Score: " + str(score), True, (0, 0, 139))
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)

def game_over():
    global score
    game_over_text = game_font.render("Game Over! Final Score: " + str(score), True, (0, 0, 139))
    win.blit(game_over_text, (canvas_width/2 - game_over_text.get_width()/2, canvas_height/2 - game_over_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    quit()


game_over()
