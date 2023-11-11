import pygame
from game.load_images import get_sprite_sheets

pygame.init()

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 2

    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_animation = 0
        self.hit_count = 0 
        self.SPRITES = get_sprite_sheets("MainCharacters", name, 32, 32, True)
        self.items = 0
        self.teleport = False
        self.teleport_aniamtion = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
    
    def make_teleport(self):
        self.teleport = True 

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_animation += 1
        if self.teleport:
            self.teleport_aniamtion += 1
        
        if self.teleport_aniamtion >= fps/4:
            self.teleport = False
            self.teleport_aniamtion = 0
            self.rect.x = 2700
            

        if self.hit_animation >= fps/2:
            self.hit = False
            self.hit_count += 1
            self.hit_animation = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = 

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        if self.teleport:
            sprites = get_sprite_sheets("MainCharacters", "State", 96, 96, True)["Desappearing (96x96)" + "_" + self.direction]
        else: 
            sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
    

class NPC(Player):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
    
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_animation += 1
        if self.teleport:
            self.teleport_aniamtion += 1
        
        if self.teleport_aniamtion >= fps:
            self.teleport = False
            self.teleport_aniamtion = 0
            self.rect.x = 2900
            
        if self.hit_animation >= fps/2:
            self.hit = False
            self.hit_count += 1
            self.hit_animation = 0

        self.fall_count += 1
        self.update_sprite()
    