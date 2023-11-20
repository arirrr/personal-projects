#created by Arir, who

import pygame
import os

# Initialize Pygame font and mixer modules
pygame.font.init()
pygame.mixer.init()

# Set the width and height of the game window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

# Define color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create a border rectangle to separate the two sides of the game window
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Define font objects for displaying health and winner text
HEALTH_FONT = pygame.font.SysFont('roboto', 40)
WINNER_FONT = pygame.font.SysFont('roboto', 100)

# Set the frames per second, spaceship velocity, bullet velocity, and maximum number of bullets
FPS = 45
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

# Set the width and height of the spaceships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Define custom events for bullet collisions
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load spaceship images for the yellow and red spaceships
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('/Users/homewithinahome/Documents/Github/homewithinahome/first-pygame/Assets', '/Users/homewithinahome/Documents/Github/homewithinahome/first-pygame/Assets/spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
  YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('/Users/homewithinahome/Documents/Github/homewithinahome/first-pygame/Assets', '/Users/homewithinahome/Documents/Github/homewithinahome/first-pygame/Assets/spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
  RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Load the background image and scale it to fit the game window
SPACE = pygame.transform.scale(pygame.image.load(
  os.path.join('/Users/homewithinahome/Documents/Github/homewithinahome/first-pygame/Assets', '/Users/homewithinahome/Documents/Github/homewithinahome/first-pygame/Assets/space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # Draw the background image, border, health text, spaceships, and bullets
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
      "HP: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
      "HP: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    # Handle movement of the yellow spaceship based on user input
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    # Handle movement of the red spaceship based on user input
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # Update bullet positions and check for collisions with spaceships
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    # Draw the winner text on the screen
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 
                        2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    # Create rectangles for the yellow and red spaceships
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = [] # Create an empty list for red bullets
    yellow_bullets = [] # Create an empty list for yellow bullets

    red_health = 3 # Set the initial health value for the red spaceship
    yellow_health = 3 # Set the initial health value for the yellow spaceship

    clock = pygame.time.Clock() # Create a clock object to control the frame rate
    run = True
    while run:
        clock.tick(FPS) # Limit the frame rate to the specified FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.y, + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()