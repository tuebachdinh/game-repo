import pygame
from game.load_images import get_sprite_sheets
from game.load_images import get_block_or_brick
pygame.init()

class Object(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block_or_brick(size, size, 0, 0)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Brick(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        block = get_block_or_brick(width, height, 0, 0)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
    
class Fire(Object):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = get_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Saw(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        self.saw = get_sprite_sheets("Traps", "Saw", width, height)
        self.image = self.saw["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.saw[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Item(pygame.sprite.Sprite):
    ANIMATION_DELAY = 2
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_count = 0 
        self.SPRITES = get_sprite_sheets("Items", "Fruits", 32, 32, False)
        self.hit = False
        self.hit_animation = 0

    def update_sprite_sheet(self):
        sprites = self.SPRITES[self.name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if (self.animation_count // self.ANIMATION_DELAY) >  len(sprites):
            self.animation_count = 0
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        if self.hit == True:
            self.name = "Collected"
            self.hit_animation += 1
            if self.hit_animation > 10:
                self.rect.x = - 100
                self.rect.y = - 100
    
    
    def loop(self, fps):
        self.update_sprite_sheet()

    def disappear(self):
        self.hit = True
    
    def draw(self, window, offset_x):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
