import pygame
import tkinter
import random
import math
import mysql.connector
from config import password
dbconfig = {'host': 'www.db4free.net',
            'user': 'ceo_of_dying',
            'password': password,
            'database': 'save_game'
            }
app = tkinter.Tk()
pygame.init()
pygame.mixer.init()
FPS = 15
WIDTH = app.winfo_screenwidth()
HEIGHT = app.winfo_screenheight()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
color = BLACK
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.music.load("Sounds/M.O.O.N._Release_Hotline_Miami_Soundtrack_ZSzoKL_iO5M_140.mp3")

sounds = [pygame.mixer.Sound("Sounds/sndHit.mp3"),
          pygame.mixer.Sound("Sounds/sndHit1.mp3"),
          pygame.mixer.Sound("Sounds/sndHit2.mp3"),
          pygame.mixer.Sound("Sounds/sndHit3.mp3")]

jacket_walking = [pygame.image.load("sprites/jacket_walk_unarmed_1.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_2.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_3.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_4.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_5.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_6.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_7.png"),
                  pygame.image.load("sprites/jacket_walk_unarmed_8.png")]

mobster_unarmed_walking = [pygame.image.load("sprites/mobster_unarmed_walking_1.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_2.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_3.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_4.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_5.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_6.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_7.png"),
                           pygame.image.load("sprites/mobster_unarmed_walking_8.png")]

mobster_bat_walking = [pygame.image.load("sprites/mafia_bat_walking_1.png"),
                       pygame.image.load("sprites/mafia_bat_walking_2.png"),
                       pygame.image.load("sprites/mafia_bat_walking_3.png"),
                       pygame.image.load("sprites/mafia_bat_walking_4.png"),
                       pygame.image.load("sprites/mafia_bat_walking_5.png"),
                       pygame.image.load("sprites/mafia_bat_walking_6.png"),
                       pygame.image.load("sprites/mafia_bat_walking_7.png"),
                       pygame.image.load("sprites/mafia_bat_walking_8.png")]

jacket_attack = [pygame.image.load("sprites/jacket_punch_1.png"),
                 pygame.image.load("sprites/jacket_punch_2.png"),
                 pygame.image.load("sprites/jacket_punch_3.png"),
                 pygame.image.load("sprites/jacket_punch_4.png"),
                 pygame.image.load("sprites/jacket_punch_5.png"),
                 pygame.image.load("sprites/jacket_punch_6.png"),
                 pygame.image.load("sprites/jacket_punch_7.png")]

mobster_bat_attack = [pygame.image.load("sprites/mobster_bat_attack_1.png"),
                      pygame.image.load("sprites/mobster_bat_attack_2.png"),
                      pygame.image.load("sprites/mobster_bat_attack_3.png"),
                      pygame.image.load("sprites/mobster_bat_attack_1.png"),
                      pygame.image.load("sprites/mobster_bat_attack_5.png"),
                      pygame.image.load("sprites/mobster_bat_attack_6.png"),
                      pygame.image.load("sprites/mobster_bat_attack_7.png"),
                      pygame.image.load("sprites/mobster_bat_attack_8.png")]

mobster_hurt = [pygame.image.load("sprites/mobster_wounded_1.png"),
                pygame.image.load("sprites/mobster_wounded_2.png"),
                pygame.image.load("sprites/mobster_wounded_3.png"),
                pygame.image.load("sprites/mobster_wounded_4.png"),
                pygame.image.load("sprites/mobster_wounded_5.png"),
                pygame.image.load("sprites/mobster_wounded_6.png"),
                pygame.image.load("sprites/mobster_wounded_7.png"),
                pygame.image.load("sprites/mobster_wounded_8.png")]

jacket_dead = [pygame.image.load("sprites/blunt_death_1.png"),
               pygame.image.load("sprites/blunt_death_2.png"),
               pygame.image.load("sprites/blunt_death_3.png")]

menu_bg = pygame.image.load("img/starting_screen.png")
background = pygame.image.load("img/level_bg.png")
tutorial_bg = pygame.image.load("img/tutorial_bg.png")

mobster_bat_list = []

mobster_unarmd_list = []
# height parameters of hostile sprites
height_bat = 190
height_unarmd = 151
# ammount of places that the sprite can take
bat_num = math.floor(HEIGHT / height_bat)

unarmd_num = math.floor(HEIGHT / height_unarmd)


def sprite_counter(height, num, list):
    for i in range(num):
        list.append(HEIGHT - height)
        height += 200


sprite_counter(height_bat, bat_num, mobster_bat_list)
sprite_counter(height_unarmd, unarmd_num, mobster_unarmd_list)
# coordinates
jckt_x = 100
jckt_y = 100
mob_bat_1_x = WIDTH - 149
mob_bat_1_y = random.choice(mobster_bat_list)
mob_bat_2_x = WIDTH - 149
mob_bat_2_y = random.choice(mobster_bat_list)
mob_bat_3_x = WIDTH - 149
mob_bat_3_y = random.choice(mobster_bat_list)
mob_unarmd_1_x = WIDTH - 99
mob_unarmd_1_y = random.choice(mobster_bat_list)
mob_unarmd_2_x = WIDTH - 99
mob_unarmd_2_y = random.choice(mobster_bat_list)

# frame numbers for animations
value_jacket_walk = 0
value_jacket_attack = 0
value_mobster_bat_walk = 0
value_mobster_unarmed_walk = 0
value_mobster_bat_attack = 0
value_mobster_hurt = 0
# misc
text = ''
game_mode = "menu"
direction = "stop"
hits = 0
frame_count = 0
font = pygame.font.SysFont('Exo', 64, bold=True)
font_small = pygame.font.SysFont('Exo', 36, bold=True)
# booleans
show_hint_0 = True
show_hint_1 = False
show_hint_2 = False
show_hint_3 = False
show_hint_4 = False
show_hint_5 = False
show_hint_6 = False
show_hint_7 = False
show_hint_8 = False
run = True
input_ready = False
pause = False
gaming_ready = False
reg = False
# buttons
start = font.render("START", True, WHITE)
exit = font.render("EXIT", True, WHITE)
tutorial = font.render("TUTORIAL", True, WHITE)

# text
hint_0 = font.render("So you haven't figured out the way to play this game. It's fairly simple.", True, WHITE)
hint_1 = font.render("You hit this guy in his face. But to do that you need to get to him.", True, WHITE)
hint_2 = font.render("See the W and S buttons?. You can use them to move up and down.", True, WHITE)
hint_3 = font.render("Trust me, there's no need to move forward or backward", True, WHITE)
hint_4 = font.render("Now go ahead and break his nose.", True, WHITE)
hint_5 = font.render("See him crawl? You don't want that to happen to you, do you?", True, WHITE)
hint_6 = font.render("If you see any big guys around here, you should avoid them", True, WHITE)
hint_7 = font.render("Try again...", True, WHITE)
hint_8 = font.render("Good job! Now click on this text and play this game, because you are ready.", True, WHITE)
greeting = font_small.render("Welcome! Please enter your name and press Enter", True, WHITE)
restart = font.render("Press Space to continue", True, WHITE)
# rect values
input_rect = pygame.Rect(WIDTH / 3, HEIGHT / 1.7, WIDTH / 3, 90)
score_rect = pygame.Rect(WIDTH /2, HEIGHT/10, WIDTH/2, 90)
restart_rect = pygame.Rect(0, HEIGHT- HEIGHT/10, WIDTH, HEIGHT/10)
menu_bg_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
tutorial_bg_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
background_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
background_rect_2 = pygame.Rect(2 * WIDTH, 0, WIDTH, HEIGHT)
jacket_walking_rect = pygame.Rect(jckt_x, jckt_y, 290, 190)
jacket_attacking_rect = pygame.Rect(jckt_x, jckt_y, 361, 216)
jacket_dead_rect = pygame.Rect(jckt_x, jckt_y, 431, 203)
mobster_bat_1_walking_rect = pygame.Rect(mob_bat_1_x, mob_bat_1_y, 140, 190)
mobster_bat_2_walking_rect = pygame.Rect(mob_bat_2_x, mob_bat_2_y, 140, 190)
mobster_bat_3_walking_rect = pygame.Rect(mob_bat_3_x, mob_bat_3_y, 140, 190)
mobster_bat_1_attack_rect = pygame.Rect(2 * WIDTH, 2 * HEIGHT, 230, 224)
mobster_bat_2_attack_rect = pygame.Rect(2 * WIDTH, 2 * HEIGHT, 230, 224)
mobster_unarmed_walking_1_rect = pygame.Rect(mob_unarmd_1_x, mob_unarmd_1_y, 99, 151)
mobster_unarmed_walking_2_rect = pygame.Rect(mob_unarmd_2_x, mob_unarmd_2_y, 99, 151)
mobster_hurt_1_rect = pygame.Rect(10 * WIDTH, mob_unarmd_1_y, 441, 151)
mobster_hurt_2_rect = pygame.Rect(3 * WIDTH, 3 * HEIGHT, 441, 151)

# rect values of text and buttons
start_rect = start.get_rect()
exit_rect = exit.get_rect()
tutorial_rect = tutorial.get_rect()
hint_rect = hint_0.get_rect()
hint_1_rect = hint_1.get_rect()
hint_2_rect = hint_2.get_rect()
hint_3_rect = hint_3.get_rect()
# placing rects
start_rect.move_ip(WIDTH / 6, HEIGHT / 10)
exit_rect.move_ip(WIDTH - WIDTH / 6, HEIGHT / 10)
tutorial_rect.move_ip(WIDTH / 2, HEIGHT - HEIGHT / 8)
hint_rect.move_ip(WIDTH / 20, HEIGHT - HEIGHT / 5)


# functions

def respawn():
    mobster_bat_1_walking_rect.y = random.choice(mobster_bat_list)
    mobster_bat_2_walking_rect.y = random.choice(mobster_bat_list)
    mobster_bat_3_walking_rect.y = random.choice(mobster_bat_list)
    mobster_unarmed_walking_1_rect.y = random.choice(mobster_bat_list)
    mobster_unarmed_walking_2_rect.y = random.choice(mobster_bat_list)
    if mobster_bat_1_walking_rect.y == mobster_bat_2_walking_rect.y or mobster_bat_1_walking_rect.y == mobster_bat_3_walking_rect.y or mobster_bat_1_walking_rect.y == mobster_unarmed_walking_1_rect.y or mobster_bat_1_walking_rect.y == mobster_unarmed_walking_2_rect.y:
        mobster_bat_1_walking_rect.y = random.choice(mobster_bat_list)
    elif mobster_bat_2_walking_rect.y == mobster_bat_1_walking_rect.y or mobster_bat_2_walking_rect.y == mobster_bat_3_walking_rect.y or mobster_bat_2_walking_rect.y == mobster_unarmed_walking_1_rect.y or mobster_bat_2_walking_rect.y == mobster_unarmed_walking_2_rect.y:
        mobster_bat_2_walking_rect.y = random.choice(mobster_bat_list)
    elif mobster_bat_3_walking_rect.y == mobster_bat_1_walking_rect.y or mobster_bat_3_walking_rect.y == mobster_bat_2_walking_rect.y or mobster_bat_3_walking_rect.y == mobster_unarmed_walking_1_rect.y or mobster_bat_3_walking_rect.y == mobster_unarmed_walking_2_rect.y:
        mobster_bat_3_walking_rect.y = random.choice(mobster_bat_list)
    elif mobster_unarmed_walking_1_rect.y == mobster_bat_1_walking_rect.y or mobster_unarmed_walking_1_rect.y == mobster_bat_2_walking_rect.y or mobster_unarmed_walking_1_rect.y == mobster_bat_3_walking_rect.y or mobster_unarmed_walking_1_rect.y == mobster_unarmed_walking_2_rect.y:
        mobster_unarmed_walking_1_rect.y = random.choice(mobster_unarmd_list)
    elif mobster_unarmed_walking_2_rect.y == mobster_bat_1_walking_rect.y or mobster_unarmed_walking_2_rect.y == mobster_bat_2_walking_rect.y or mobster_unarmed_walking_2_rect.y == mobster_bat_3_walking_rect.y or mobster_unarmed_walking_2_rect.y == mobster_unarmed_walking_1_rect.y:
        mobster_unarmed_walking_2_rect.y = random.choice(mobster_unarmd_list)
    else:
        mobster_bat_1_walking_rect.update(WIDTH, mobster_bat_1_walking_rect.y, 140, 190)
        mobster_bat_2_walking_rect.update(WIDTH, mobster_bat_2_walking_rect.y, 140, 190)
        mobster_bat_3_walking_rect.update(WIDTH, mobster_bat_3_walking_rect.y, 140, 190)
        mobster_unarmed_walking_1_rect.update(WIDTH, mobster_unarmed_walking_1_rect.y, 99, 151)
        mobster_unarmed_walking_2_rect.update(WIDTH, mobster_unarmed_walking_2_rect.y, 99, 151)
        mobster_hurt_1_rect.update(WIDTH * 4, mobster_hurt_1_rect.y, 441, 151)

def beaten(rect):
    anim_mobster_bat_attack(rect)
    random.choice(sounds).play()
    jacket_dead_rect.update(jacket_walking_rect.x, jacket_walking_rect.y, 431, 155)
    screen.blit(random.choice(jacket_dead), jacket_dead_rect)

def anim_jacket_walk():
    global value_jacket_walk
    image = jacket_walking[value_jacket_walk]
    screen.blit(image, jacket_walking_rect)
    value_jacket_walk += 1
    if value_jacket_walk >= len(jacket_walking):
        value_jacket_walk = 0


def anim_jacket_attack():
    global value_jacket_attack
    image = jacket_attack[value_jacket_attack]
    screen.blit(image, jacket_walking_rect)
    value_jacket_attack += 1
    if value_jacket_attack >= len(jacket_attack):
        value_jacket_attack = 0


def anim_mobster_bat_walk(rect):
    global value_mobster_bat_walk
    image = mobster_bat_walking[value_mobster_bat_walk]
    screen.blit(image, rect)
    value_mobster_bat_walk += 1
    if value_mobster_bat_walk >= len(mobster_bat_walking):
        value_mobster_bat_walk = 0


def anim_mobster_unarmed_walk(rect):
    global value_mobster_unarmed_walk
    image = mobster_unarmed_walking[value_mobster_unarmed_walk]
    screen.blit(image, rect)
    value_mobster_unarmed_walk += 1
    if value_mobster_unarmed_walk >= len(mobster_unarmed_walking):
        value_mobster_unarmed_walk = 0


def anim_mobster_bat_attack(rect):
    global value_mobster_bat_attack
    image = mobster_bat_attack[value_mobster_bat_attack]
    screen.blit(image, rect)
    value_mobster_bat_attack += 1
    if value_mobster_bat_attack >= len(mobster_bat_attack):
        value_mobster_bat_attack = 0


def anim_mobster_hurt(rect):
    global value_mobster_hurt
    image = mobster_hurt[value_mobster_hurt]
    screen.blit(image, rect)
    value_mobster_hurt += 1
    if value_mobster_hurt >= len(mobster_hurt):
        value_mobster_hurt = 0

#music is here
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)
while run:

    screen.blit(background, background_rect)
    screen.blit(background, background_rect_2)
    if background_rect.right >= 0:
        background_rect.left -= 50
        background_rect_2.left -= 50
    if background_rect.right <= 0:
        background_rect.right = WIDTH
        background_rect_2.right = 2 * WIDTH

    if game_mode == "menu":
        screen.blit(menu_bg, menu_bg_rect)
        screen.blit(start, start_rect)
        screen.blit(tutorial, tutorial_rect)
        screen.blit(exit, exit_rect)
        txt_surface = font.render(text, True, GREEN)
        width = max(600, txt_surface.get_width() + 10)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, color, input_rect, 4)
        screen.blit(greeting, (input_rect.x + 5, input_rect.y + 30))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if start_rect.collidepoint(i.pos) and gaming_ready:
                        game_mode = "game"
                        respawn()
                    elif tutorial_rect.collidepoint(i.pos):
                        game_mode = "tutorial"
                    elif exit_rect.collidepoint(i.pos):
                        pygame.quit()
                    elif input_rect.collidepoint(i.pos):
                        input_ready = True
                        color = GREEN
                        greeting = font_small.render("", True, BLACK)
                    else:
                        input_ready = False
                        color = BLACK


            if i.type == pygame.KEYDOWN:
                if input_ready:
                    if i.key == pygame.K_RETURN:
                        gaming_ready = True
                        conn = mysql.connector.connect(**dbconfig)
                        cursor = conn.cursor()
                        _SQL = '''select id from users where name = (%s)'''
                        cursor.execute(_SQL, (text,))
                        id = cursor.fetchall()
                        if len(id) == 0:
                            reg = True
                            _SQL = '''insert into users (name) values (%s)'''
                            cursor.execute(_SQL, (text,))
                            conn.commit()
                            _SQL = '''select id from users where name = (%s)'''
                            cursor.execute(_SQL, (text,))
                            id = cursor.fetchall()
                            cursor.close()
                            conn.close()
                    elif i.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += i.unicode

    if game_mode == "tutorial":
        screen.blit(tutorial_bg, tutorial_bg_rect)
        anim_mobster_hurt(mobster_hurt_1_rect)
        anim_mobster_unarmed_walk(mobster_unarmed_walking_1_rect)
        anim_jacket_walk()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if tutorial_bg_rect.collidepoint(i.pos) and show_hint_0 == True:
                        show_hint_0 = False
                        show_hint_1 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_1:
                        show_hint_1 = False
                        show_hint_2 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_2:
                        show_hint_2 = False
                        show_hint_3 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_3:
                        show_hint_3 = False
                        show_hint_4 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_4:
                        show_hint_4 = False
                        show_hint_5 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_5:
                        show_hint_5 = False
                        show_hint_6 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_6:
                        show_hint_6 = False
                        show_hint_7 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_7:
                        show_hint_7 = False
                        show_hint_8 = True
                    elif tutorial_bg_rect.collidepoint(i.pos) and show_hint_8:
                        show_hint_8 = False
                        game_mode = "menu"
                    elif tutorial_bg_rect.collidepoint(i.pos):
                        game_mode = "menu"

            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_w:
                    direction = "up"
                elif i.key == pygame.K_s:
                    direction = "down"
                elif i.key == pygame.K_UP:
                    direction = "up"
                elif i.key == pygame.K_DOWN:
                    direction = "down"
            elif i.type == pygame.KEYUP:
                direction = "stop"

        if direction == "up" and jacket_walking_rect.top > 20:
            jacket_walking_rect.top -= 25

        elif direction == "down" and jacket_walking_rect.bottom < HEIGHT - 20:
            jacket_walking_rect.bottom += 25

        if mobster_unarmed_walking_1_rect.right > -100:
            mobster_unarmed_walking_1_rect.right -= 50
        elif mobster_unarmed_walking_1_rect.right <= -100:
            mobster_unarmed_walking_1_rect.update(WIDTH, mobster_unarmed_walking_1_rect.y, 99, 151)
        if mobster_hurt_1_rect.right > -500:
            mobster_hurt_1_rect.right -= 25
        elif mobster_hurt_1_rect.right < 0:
            mobster_unarmed_walking_1_rect.update(WIDTH, mobster_unarmed_walking_1_rect.y, 99, 151)
        if jacket_walking_rect.colliderect(mobster_unarmed_walking_1_rect):
            anim_jacket_attack()
            random.choice(sounds).play()
            mobster_hurt_1_rect.update(mobster_unarmed_walking_1_rect.right, mobster_unarmed_walking_1_rect.top, 432,
                                       207)
            mobster_unarmed_walking_1_rect.update(2 * WIDTH, mobster_unarmed_walking_1_rect.y, 99, 151)
        if show_hint_0:
            screen.blit(hint_0, hint_rect)
        elif show_hint_1:
            screen.blit(hint_1, hint_rect)
        elif show_hint_2:
            screen.blit(hint_2, hint_rect)
        elif show_hint_3:
            screen.blit(hint_3, hint_rect)
        elif show_hint_4:
            screen.blit(hint_4, hint_rect)
        elif show_hint_5:
            screen.blit(hint_5, hint_rect)
        elif show_hint_6:
            screen.blit(hint_6, hint_rect)
        elif show_hint_7:
            screen.blit(hint_7, hint_rect)
        elif show_hint_8:
            screen.blit(hint_8, hint_rect)

    if game_mode == "game":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_w:
                    direction = "up"
                elif i.key == pygame.K_s:
                    direction = "down"
                elif i.key == pygame.K_UP:
                    direction = "up"
                elif i.key == pygame.K_DOWN:
                    direction = "down"
            elif i.type == pygame.KEYUP:
                direction = "stop"

        if direction == "up" and jacket_walking_rect.top > 20:
            jacket_walking_rect.top -= 15

        elif direction == "down" and jacket_walking_rect.bottom < HEIGHT - 20:
            jacket_walking_rect.bottom += 15
            
        if mobster_hurt_1_rect.right > -150 and pause == False:
            mobster_hurt_1_rect.right -= 25

        if mobster_bat_1_walking_rect.right > -150 and pause == False:
            mobster_bat_1_walking_rect.right -= 45
        elif mobster_bat_1_walking_rect.x <= 0:
            respawn()

        if mobster_bat_2_walking_rect.right > -150 and pause == False:
            mobster_bat_2_walking_rect.right -= 45
        elif mobster_unarmed_walking_2_rect.x <= 0:
            respawn()

        if mobster_unarmed_walking_1_rect.x > -100:
            mobster_unarmed_walking_1_rect.x -= 45
        elif mobster_unarmed_walking_1_rect.x <= 0:
            respawn()
        if mobster_unarmed_walking_2_rect.x > -100:
            mobster_unarmed_walking_2_rect.x -= 45
        elif mobster_unarmed_walking_2_rect.x <= 0:
            respawn()
        if jacket_walking_rect.colliderect(mobster_bat_1_walking_rect):
            pause = True
            beaten(mobster_bat_1_walking_rect)
            conn = mysql.connector.connect(**dbconfig)
            cursor = conn.cursor()
            _SQL = '''insert into scores (user_id, score) values (%s, %s)'''
            cursor.execute(_SQL, (id[0][0], hits))
            conn.commit()
            cursor.close()
            conn.close()
            game_mode = "game_over"
        if jacket_walking_rect.colliderect(mobster_bat_2_walking_rect):
            pause = True
            beaten(mobster_bat_2_walking_rect)
            conn = mysql.connector.connect(**dbconfig)
            cursor = conn.cursor()
            _SQL = '''insert into scores (user_id, score) values (%s, %s)'''
            cursor.execute(_SQL, (id[0][0], hits))
            conn.commit()
            cursor.close()
            conn.close()
            game_mode = "game_over"
        if jacket_walking_rect.colliderect(mobster_unarmed_walking_1_rect):
            anim_jacket_attack()
            random.choice(sounds).play
            mobster_hurt_1_rect.update(mobster_unarmed_walking_1_rect.right, mobster_unarmed_walking_1_rect.top, 432,
                                       207)
            mobster_unarmed_walking_1_rect.update(mobster_unarmed_walking_2_rect.x, HEIGHT * 2, 99, 151)
            hits += 1
        if jacket_walking_rect.colliderect(mobster_unarmed_walking_2_rect):
            anim_jacket_attack()
            random.choice(sounds).play
            mobster_hurt_1_rect.update(mobster_unarmed_walking_2_rect.right, mobster_unarmed_walking_2_rect.top, 432,
                                       207)
            mobster_unarmed_walking_2_rect.update(mobster_unarmed_walking_2_rect.x,HEIGHT * 2, 99, 151)
            hits += 1



        anim_mobster_unarmed_walk(mobster_unarmed_walking_1_rect)
        anim_mobster_unarmed_walk(mobster_unarmed_walking_2_rect)
        anim_mobster_hurt(mobster_hurt_1_rect)
        anim_mobster_unarmed_walk(mobster_unarmed_walking_1_rect)
        anim_mobster_unarmed_walk(mobster_unarmed_walking_2_rect)
        anim_mobster_bat_walk(mobster_bat_1_walking_rect)
        anim_mobster_bat_walk(mobster_bat_2_walking_rect)
        anim_jacket_walk()

    elif game_mode == "game_over":
        score = font.render("You've beaten " + str(hits) + " mobsters this round", True, WHITE)
        pygame.draw.rect(screen, BLACK, score_rect)
        pygame.draw.rect(screen, BLACK, restart_rect)
        screen.blit(score, (score_rect.x + 10, score_rect.y + 20))
        screen.blit(restart, (restart_rect.x + 30, restart_rect.y + 30))
        frame_count = 0

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    run = False
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
