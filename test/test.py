from os.path import join
import pygame

pygame.init()

# Define your screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Background Scrolling Example")

background = pygame.Surface((800, 600))
background_scroll_x = 0  # Initial x-coordinate for scrolling
background_scroll_speed = 1  # Adjust as needed

running = True
clock = pygame.time.Clock()

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image
tiles, image = get_background("Blue.png")
for tile in tiles:
 background.blit(image, tile)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    # Scroll the background
    background_scroll_x -= background_scroll_speed

    # If the background goes completely off-screen, reset its position
    if background_scroll_x < -background.get_width():
        background_scroll_x = 0

    # Clear the screen
    screen.fill((0, 0, 0))
  
    # Draw the background twice to achieve the scrolling effect
    screen.blit(background, (background_scroll_x, 0))
    screen.blit(background, (background_scroll_x + background.get_width(), 0))

    # Update the display
    pygame.display.update()

    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()