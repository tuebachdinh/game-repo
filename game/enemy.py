import pygame
from game.load_images import get_sprite_sheets, run_sprites

pygame.init()
class Enemy(pygame.sprite.Sprite):
    ANIMATION_DELAY = 4
    def __init__(self, x, y, width, height, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.animation_count = 0
        self.hit = False
        self.hit_animation = 0 
    
    def draw(self, window, offset_x):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
    
    def disappear(self):
        self.rect.x = - 100
        self.rect.y = - 100
    def loop(self, fps):
        self.update_sprite_sheet()
        if self.hit: 
            self.hit_animation += 1
        if self.hit_animation > fps:
            self.disappear()

class Bat(Enemy):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies",name, 46, 30, True)
        self.condition = 0 
        self.delay = {0: 3, 1: 1/2, 2: 8, 3: 8, 4: 1/2, 5: 3}
    
    def update_sprite_sheet(self):
        sprite_sheet = ["Idle (46x30)_right", "Ceiling Out (46x30)_right", "Flying (46x30)_right", "Flying (46x30)_left", "Ceiling In (46x30)_left", "Idle (46x30)_left"]
        if self.hit:
            sprite_sheet_name = "Hit (46x30)_right"
        else:
            sprite_sheet_name = sprite_sheet[self.condition]
        
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if (self.animation_count // self.ANIMATION_DELAY) >  (len(sprites) * self.delay[self.condition]):
            self.condition = (self.condition + 1) % len(sprite_sheet)
            self.animation_count = 0
       
        if self.condition == 2:
            self.rect.x -= 2
        elif self.condition == 3:
            self.rect.x += 2
        
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
class Ghost(Enemy):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies",name, 44, 30, True)
        self.condition = 0 
        self.delay = {0: 2, 1: 1, 2: 3, 3: 1, 4: 3, 5: 2}
    def update_sprite_sheet(self):
        sprite_sheet = ["Idle (44x30)_right", "Desappear (44x30)_right", "Appear (44x30)_right", "Desappear (44x30)_left", "Appear (44x30)_left", "Idle (44x30)_left"]
        if self.hit:
            sprite_sheet_name = "Hit (44x30)_right"
        else:
            sprite_sheet_name = sprite_sheet[self.condition]
        
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if (self.animation_count // self.ANIMATION_DELAY) >  (len(sprites) * self.delay[self.condition]):
            self.condition = (self.condition + 1) % len(sprite_sheet)
            self.animation_count = 0
       
        if self.condition == 1:
            self.rect.x -= 16
        elif self.condition == 3:
            self.rect.x += 16
        
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    
class FatBird(Enemy):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies",name, 40, 48, False)
        self.condition = 0 
        self.delay = {0: 3, 1: 1/2, 2: 8, 3: 8, 4: 1/2, 5: 3}
        self.found_player = False
        self.landed = False
        self.fall_count = 0

    
    def update_sprite_sheet(self):
        if self.found_player: 
            sprite_sheet_name = "Fall (40x48)"
        elif self.landed: 
            sprite_sheet_name = "Idle (40x48)"
        elif self.hit:
            sprite_sheet_name = "Hit (40x48)"
        else:
            sprite_sheet_name = "Idle (40x48)"
        
        run_sprites(self, sprite_sheet_name)
    
    def loop(self, fps):
        if self.found_player:
            self.rect.y += self.fall_count
            self.fall_count += 3
        self.update_sprite_sheet()
        if self.hit: 
            self.hit_animation += 1
        if self.hit_animation > fps:
            self.disappear()


class Rino(Enemy):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies", name, 52, 34, True)
        self.condition = 0 
        self.delay = {0: 2, 1: 4, 2: 4, 3: 2}

    def update_sprite_sheet(self):
        sprite_sheet = ["Idle (52x34)_right", "Run (52x34)_right", "Run (52x34)_left", "Idle (52x34)_left"]
        if self.hit:
            sprite_sheet_name = "Hit (52x34)_right"
        else:
            sprite_sheet_name = sprite_sheet[self.condition]
        
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if (self.animation_count // self.ANIMATION_DELAY) >  (len(sprites) * self.delay[self.condition]):
            self.condition = (self.condition + 1) % len(sprite_sheet)
            self.animation_count = 0
        
        if self.condition == 1:
            self.rect.x -= 2
        elif self.condition == 2:
            self.rect.x += 2
        
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

class Chameleon(Enemy):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies", name, 84, 38, True)
        self.condition = 0 
        self.delay = {0: 2, 1: 4}

    def update_sprite_sheet(self):
        sprite_sheet = ["Idle (84x38)_right", "Attack (84x38)_right"]
        if self.hit:
            sprite_sheet_name = "Hit (84x38)_right"
        else:
            sprite_sheet_name = sprite_sheet[self.condition]
        
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if (self.animation_count // self.ANIMATION_DELAY) >  (len(sprites) * self.delay[self.condition]):
            self.condition = (self.condition + 1) % len(sprite_sheet)
            self.animation_count = 0

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


class BlueBird(Enemy):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies", name, 32, 32, True)
        self.direction = "left"
        self.x_vel = 0
        self.y_vel = 0

    def update_sprite_sheet(self):
        if self.hit:
            sprite_sheet_name = "Hit (32x32)_" + self.direction
        else:
            sprite_sheet_name = "Flying (32x32)_" + self.direction
       
        run_sprites(self, sprite_sheet_name)
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    def loop(self, fps):
        self.update_sprite_sheet()
        if self.hit: 
            self.hit_animation += 1

class Turtle(BlueBird):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies", name, 44, 26, True)
        self.direction = "left"
    
    def update_sprite_sheet(self):
        if self.hit:
            sprite_sheet_name = "Hit (44x26)_" + self.direction
        else:
            sprite_sheet_name = "Idle 1 (44x26)_" + self.direction
       
        run_sprites(self, sprite_sheet_name)

class Bunny(BlueBird):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies", name, 34, 44, True)
        self.direction = "left"
    
    def update_sprite_sheet(self):
        sprite_sheet_name = "Idle (34x44)_" + self.direction
        if self.hit:
            sprite_sheet_name = "Hit (34x44)_" + self.direction
        elif self.x_vel != 0:
            sprite_sheet_name = "Run (34x44)_" + self.direction
       
        run_sprites(self, sprite_sheet_name)

class Radish(BlueBird):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.SPRITES = get_sprite_sheets("Enemies", name, 30, 38, True)
        self.direction = "left"
    
    def update_sprite_sheet(self):
        sprite_sheet_name = "Idle 1 (30x38)_" + self.direction
        if self.hit:
            sprite_sheet_name = "Hit (30x38)_" + self.direction
        elif self.x_vel != 0:
            sprite_sheet_name = "Run (30x38)_" + self.direction
       
        run_sprites(self, sprite_sheet_name)



    