from pygame import *

# Initialize Pygame
init()

# Set the window size
size = (800, 600)

# Create the screen
screen = display.set_mode(size)

# Load the font
ARIAL_50 = font.SysFont('arial', 50)

# Define the menu class
class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(ARIAL_50.render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces)-1))


    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y+i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

# Define the game class
class Game:
    def __init__(self):
        self.score = 0
        self.game_over = False

    def handle_events(pygame, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()

    def update(game):
        if game.state == "playing":
            game.update_objects()
            game.check_collisions()
            game.spawn_objects()


    def draw(game, pygame):
        game.screen.fill((255, 255, 255))
        if game.state == "menu":
            game.draw_menu()
        elif game.state == "playing":
            game.draw_objects()
            game.draw_score()
        pygame.display.update()

# Create instances of the Menu and Game classes
menu = Menu()
menu.append_option('Start the game', Game)
menu.append_option('Quit', quit)

game = None

# Main game loop
running = True
while running:

    for event in event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_w:
                menu.switch(-1)
            elif event.key == K_s:
                menu.switch(1)
            elif event.key == K_SPACE:
                menu.select()

    screen.fill((0, 0, 0))

    if game is None:
        # Show the menu if no game is active
        menu.draw(screen, 100, 100, 75)
    else:
        # Otherwise, update and draw the game
        game.handle_events()
        game.update()
        game.draw(screen)

    # Update the display
    display.flip()

    # Start the game if the "Start the game" option is selected
    if menu._current_option_index == 0 and game is None:
        game = Game()

# Quit Pygame
quit()
