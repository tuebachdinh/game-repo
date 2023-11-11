import pygame
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT = 1152, 768

pygame.init()

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    background = pygame.Surface((WIDTH, HEIGHT))

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
            background.blit(image, pos)

    return background.convert()

def get_sprite_sheets(dir1, dir2, width, height, direction = False):
    def flip(sprites): 
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block_or_brick(size1, size2, pos1, pos2):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size1, size2), pygame.SRCALPHA, 32)
    rect = pygame.Rect(pos1, pos2, size1, size2)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_condition_bar(player):
    condition_bar = pygame.transform.scale(pygame.image.load(join("state","condition_bar.png")), (320, 150))
    full_heart = pygame.transform.scale(pygame.image.load(join("state","full_heart.png")), (45, 45))

    if player.hit_count == 0:
        lives = pygame.font.Font(join("assets","Font", "Pixeltype.ttf"), 40).render("LIVES 3", True, "WHITE")
        condition_bar.blit(full_heart, (120, 50))
        condition_bar.blit(full_heart, (170, 50))
        condition_bar.blit(full_heart, (220, 50))
        condition_bar.blit(lives,(130, 100))
    elif player.hit_count == 1:
        lives = pygame.font.Font(join("assets","Font", "Pixeltype.ttf"), 40).render("LIVES 2", True, "WHITE")
        condition_bar.blit(full_heart, (120, 50))
        condition_bar.blit(full_heart, (170, 50))
        condition_bar.blit(lives,(130, 100))
    elif player.hit_count == 2:
        lives = pygame.font.Font(join("assets","Font", "Pixeltype.ttf"), 40).render("LIVES 1", True, "WHITE")
        condition_bar.blit(full_heart, (120, 50))
        condition_bar.blit(lives,(130, 100))
    elif player.hit_count == 3:
        lives = pygame.font.Font(join("assets","Font", "Pixeltype.ttf"), 40).render("LIVES 0", True, "WHITE")
        condition_bar.blit(lives,(130, 100))
    
    return condition_bar

