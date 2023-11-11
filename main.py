import pygame
from os import listdir
from os.path import isfile, join
from game.player import Player, NPC
from game.enemy import Bat, BlueBird, Rino, Chameleon, Turtle
from game.load_images import get_background, get_condition_bar
from game.object import Block, Brick, Item, Fire, Saw

pygame.init()

# Set up 
WIDTH, HEIGHT = 1152, 768
FPS = 60
PLAYER_VEL = 5
music = pygame.mixer.music.load(join("sound","music.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tue_PyGame")
isStart = True


# Handle interactions between player, objects, pets and enemies
def handle_vertical_collision(player, objects, enemies, dy):
    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)
    
    for enemy in enemies:
        if pygame.sprite.collide_mask(player, enemy):
            if dy > 8 :
                player.rect.bottom = enemy.rect.top
                player.landed()
            elif dy < -8:
                player.rect.top = enemy.rect.bottom
                player.hit_head()

            collided_objects.append(enemy)

    return collided_objects

def handle_horizontal_collide(player, objects, enemies, pet1, pet2, items, dx):
    player.move(dx, 0)
    player_collided = []
    player_received = []
    pet1_collided = []
    pet2_collided = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            player_collided.append(obj)
    
    for item in items:
        if pygame.sprite.collide_mask(player, item):
            player_received.append(item)
   
    for enemy in enemies:
        if pygame.sprite.collide_mask(player, enemy):
            player_collided.append(enemy)
        if pygame.sprite.collide_mask(pet1, enemy):
            pet1_collided.append(enemy)
        if pygame.sprite.collide_mask(pet2, enemy):
            pet2_collided.append(enemy)
            
    player.move(-dx, 0)
    return player_collided, player_received, pet1_collided, pet2_collided

def handle_move(player, npc, objects, enemies, pet1, pet2, items):
    hit_sound = pygame.mixer.Sound(join("sound","hit.mp3"))
    collect_sound = pygame.mixer.Sound(join("sound","collect.mp3"))
    teleport_sound = pygame.mixer.Sound(join("sound","teleport.mp3"))
    keys = pygame.key.get_pressed()
    pet1.x_vel = 0
    pet2.x_vel = 0
    player.x_vel = 0
    npc.x_vel = 0 

    player_collided1, player_received1, pet1_collided1, pet2_collided1 = handle_horizontal_collide(player, objects, enemies, pet1, pet2, items, -PLAYER_VEL*3)
    player_collided2, player_received2, pet1_collided2, pet2_collided2 = handle_horizontal_collide(player, objects, enemies, pet1, pet2, items, PLAYER_VEL*3)

    if npc.rect.x > 2500 and keys[pygame.K_a]:
            npc.move_left(PLAYER_VEL)
   
    if npc.rect.x > 2500 and keys[pygame.K_d]:
            npc.move_right(PLAYER_VEL)
    
    if keys[pygame.K_LEFT] and len(player_collided1) == 0:
            player.move_left(PLAYER_VEL)
            pet1.move_left(PLAYER_VEL)
            pet2.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and len(player_collided2) == 0:
            player.move_right(PLAYER_VEL)
            pet1.move_right(PLAYER_VEL)
            pet2.move_right(PLAYER_VEL)

    player_collided_vertically = handle_vertical_collision(player, objects, enemies, player.y_vel)
    to_check_player = [*player_collided1, *player_collided1, *player_collided_vertically]
    to_check_pet1 = [*pet1_collided1, *pet1_collided2]
    to_check_pet2 = [*pet2_collided1, *pet2_collided2]
    to_check_item = [*player_received2, *player_received1]

    for obj in to_check_player:
        if obj.name == "fire" or obj.name == "saw" or obj.name == "Bat" or obj.name == "Rino" or obj.name == "Chamelon":
            player.make_hit()
            hit_sound.play()
    for item in to_check_item: 
        if item.name == "Apple" or item.name == "Bananas" or item.name == "Kiwi" or item.name == "Melon":
            item.disappear()
            collect_sound.play()
            player.items += 1
    
    for enemy in to_check_pet1:
        if enemy.name == "Bat" or enemy.name == "Rino" or enemy.name == "Chameleon":
            pet1.make_hit()
            if pet1.hit_animation == 1:
                hit_sound.play()
            enemy.hit = True
    for enemy in to_check_pet2:
        if enemy.name == "Bat" or enemy.name == "Rino" or enemy.name == "Chameleon":
            pet2.make_hit()
            if pet1.hit_animation == 1:
                hit_sound.play()
            enemy.hit = True

    if pygame.sprite.collide_mask(player, npc) and player.rect.x < 2500:
        player.make_teleport()
        npc.make_teleport()
        teleport_sound.play()
    
    




# Draw everything on the screen
def draw(window, background, player, npc, enemies, pet1, pet2, items, objects, offset_x, background_scroll_x, condition_bar):
    window.blit(background, (background_scroll_x, 0))
    window.blit(background, (background_scroll_x + background.get_width(), 0))

    for obj in objects:
        obj.draw(window, offset_x)

    for enemy in enemies:
        enemy.draw(window, offset_x)
    player.draw(window, offset_x)
    npc.draw(window, offset_x)
    pet1.draw(window, offset_x)
    pet2.draw(window, offset_x)
    for item in items: item.draw(window, offset_x)

    window.blit(condition_bar, (-16, HEIGHT - condition_bar.get_height() + 20 ))
    
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background = get_background("Blue.png")
    block_size = 96
    player = Player(100, 100, 50, 50, "VirtualGuy")
    npc = NPC(200 , HEIGHT - block_size*5, 50, 50, "PinkMan")
    enemies = [Bat(i*100, block_size, 50, 50, "Bat") for i in range (6,7)] +  [Rino(block_size*19, HEIGHT - block_size*4 - 68, 50, 50, "Rino")] + [Chameleon(block_size*23+24,HEIGHT - block_size*3 + 20, 50, 50, "Chameleon")]
    pet1 = BlueBird(-135, 530, 50, 50, "BlueBird")
    pet2 = Turtle(block_size*14+8,block_size+45,50,50, "Turtle")
    items = [Item(100+ i*50,200,50,50,"Apple") for i in range (8,15)] + [Item(150 + i*50, HEIGHT - block_size * 5,50,50,"Bananas") for i in range (7,14)] + [Item(1665 +i*150, HEIGHT - block_size - 64,50,50, "Kiwi") for i in range (0,3)] + [Item(block_size*14+20, block_size*3,50,50,"Kiwi"),
             Item(block_size*24+16, HEIGHT - block_size*4+48,50,50,"Melon")]
    obstacles = [Fire(-160, HEIGHT - block_size - 64, 16, 32), Fire(6*block_size +80,HEIGHT - 3*block_size - 64, 16, 32),
                 Fire(-80, HEIGHT - block_size - 64, 16, 32)] + [Saw(400 + 80*i, HEIGHT - block_size - 72, 38, 38) for i in range (0,8)] + [Fire(1600 + i*150, HEIGHT - block_size - 64, 16, 32) for i in range (0, 4)]
    wall_1 = [Block(0, i * block_size, block_size) for i in range(0, HEIGHT//block_size)]
    wall_2 = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH//block_size, 3*WIDTH// block_size)]
    wall_3 = [Block(25*block_size, i * block_size, block_size) for i in range(0, HEIGHT//block_size)]
    wall_4 = [Block(i * block_size, 0, block_size) for i in range(-WIDTH//block_size, 3*WIDTH// block_size)]
    bricks = [Brick(block_size * 4 + i * 96, HEIGHT - block_size*5 - 30, 96, 18) for i in range(0, 6)  ]
    objects = [*wall_1,*wall_2,*wall_3, *wall_4, *obstacles, *bricks]  + [Block(block_size * i, HEIGHT - block_size * (i+1), block_size) for i in range (1,4)]  + [Block(-block_size, HEIGHT - 4*block_size, block_size),
    Block(-2*block_size, HEIGHT - 4*block_size, block_size), Block(-3*block_size, HEIGHT - 4*block_size, block_size), Block(-3*block_size, HEIGHT - 3*block_size, block_size),
    Block(-3*block_size, HEIGHT - 2*block_size, block_size)] + [Block(block_size*i, HEIGHT - (14-i)*block_size, block_size) for i in range (10,13)] + [Block(block_size*15, block_size, block_size),
    Block(15*block_size, 2*block_size, block_size)] + [Block(15*block_size, i*block_size, block_size) for i in range(3,5)] + [Block(i*block_size, 4*block_size, block_size) for i in range(16, 23)] + [Block(24*block_size, HEIGHT - 2*block_size, block_size),
    Block(6*block_size, HEIGHT - 3*block_size, block_size), Block(7*block_size, HEIGHT - 3*block_size, block_size)] + [Block(block_size*13,block_size, block_size), Block(block_size*16,block_size*3, block_size),
    Block(block_size*13,block_size*2, block_size),Block(block_size*14,block_size*2, block_size)]


    offset_x = 0
    scroll_area_width = 450
    background_scroll_x = 0  
    background_scroll_speed = 2

    run = True
    while run:

        condition_bar = get_condition_bar(player)
        clock.tick(FPS)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP)and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_w and npc.jump_count < 2 and npc.rect.x > 2500:
                    npc.jump()
                   
        
        background_scroll_x -= background_scroll_speed
        if background_scroll_x < -background.get_width():
            background_scroll_x = 0
       
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        
        if npc.rect.x > 2500:
            if ((npc.rect.right - offset_x >= WIDTH - scroll_area_width) and npc.x_vel > 0) or (
                    (npc.rect.left - offset_x <= scroll_area_width) and npc.x_vel < 0):
                offset_x += npc.x_vel
        
        if player.rect.x == 2700:
            if offset_x < 2300:
                offset_x += 100
        
        for enemy in enemies: enemy.loop(FPS)
        player.loop(FPS)
        npc.loop(FPS)
        pet1.loop(FPS)
        pet2.loop(FPS)
        for obs in obstacles: obs.loop()
        for item in items: item.loop(FPS)
        
        handle_move(player, npc, objects, enemies, pet1, pet2, items)
        
        handle_vertical_collision(npc, objects, enemies, npc.y_vel)
        
        if (player.items >= 8 and not pet1.hit) or (pet1.hit and pet1.hit_animation < FPS):
                pet1.rect.x = player.rect.x + 45 
                pet1.rect.y = player.rect.y - 42 
        elif pet1.hit and pet1.hit_animation > FPS: 
                pet1.disappear()     

        
        if (player.items >= 14 and not pet2.hit) or (pet2.hit and pet2.hit_animation < FPS):
                pet2.rect.x = player.rect.x - 84 
                pet2.rect.y = player.rect.y + 16
        elif pet2.hit and pet2.hit_animation > FPS: 
                pet2.disappear()     

                

       
        draw(window, background, player, npc, enemies, pet1, pet2, items, objects, offset_x, background_scroll_x, condition_bar)

        while player.hit_count == 4:
            game_over = pygame.transform.scale((pygame.image.load(join("state","game_over.png"))), (570, 490))
            quit_image = pygame.transform.scale(pygame.image.load(join("state","quit.png")), (120, 60))
            restart_image = pygame.transform.scale(pygame.image.load(join("state","restart.png")), (180, 60))
            quit_rect = quit_image.get_rect(center = (690, 480))
            restart_rect = quit_image.get_rect(center = (480, 480))
        
            window.blit(game_over, (300, 150))
            window.blit(quit_image, (quit_rect.x, quit_rect.y))
            window.blit(restart_image, (restart_rect.x, restart_rect.y))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        main(window)
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        quit()
        

# Menu at the beginning of the game
while isStart:
    start = pygame.transform.scale(pygame.image.load(join("state","start.png")), (240,80))
    start_rect = start.get_rect(center = (600,425))
    background_start = pygame.transform.scale(pygame.image.load(join("state","background_start.jpeg")), (1200,750))
    window.blit(background_start, (0,0))
    window.blit(start, (start_rect.x, start_rect.y))
    text1 = pygame.font.Font(join("assets","Font", "Pixeltype.ttf"), 20).render("DIRECTED BY TUE DINH (TOBY)", True, "Black")
    text2 = pygame.font.Font(join("assets","Font", "Pixeltype.ttf"), 20).render("NOVEMBER 2023", True, "Black")
            
    window.blit(text1, (10,10))
    window.blit(text2, (30,30))
    pygame.display.update()

    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main(window)
                isStart = False
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
<<<<<<< HEAD
=======


>>>>>>> 714b7c2cb450325a238ad75cc2c9605755b52051



        

