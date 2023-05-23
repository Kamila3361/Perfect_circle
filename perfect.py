import pygame
import math
import time
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Perfect Circle")

# Score
score_val = 0.00
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 368
textY = 358

# Create a surface
surface_width = 128
surface_height = 32
surface = pygame.Surface((surface_width, surface_height))

#drawing tools
GREEN = (0, 225, 0)
RED = (225, 0, 0)
YELLOW = (225, 225, 0)
WHITE = (225, 225, 225)
drawing = False
last_pos = None
main_dot = None
total_sum = 0
count = 0

#over game tools
game_over = False
angle = 0
arc_length = 0
rad_sum = 0

#Error tools
error_font = pygame.font.Font('freesansbold.ttf', 64)
is_error = False
allow_drawing = True


def color_of_line(last_pos, current_pos):
    main_rad = math.sqrt(math.pow(last_pos[0] - 400, 2) + math.pow(last_pos[1] - 400, 2))
    after_rad = math.sqrt(math.pow(current_pos[0] - 400, 2) + math.pow(current_pos[1] - 400, 2)) 
    if main_rad - 20.0 <= after_rad and after_rad <= main_rad + 20.00:
        return (0, 225, 0)
    if after_rad > main_rad + 30.00:
        return (225, 0, 0)
    if after_rad < main_rad - 30.00:
        return (225, 0, 0)
    if after_rad > main_rad + 20.00:
        return (225, 225, 0)
    if after_rad < main_rad - 20.00:
        return (225, 225, 0)
    
def count_score(total_sum, count, main_dot_val):
    std = math.sqrt(total_sum / count)
    percentage = abs(100 - (std/main_dot_val) * 100) 
    return round(percentage, 1)

def show_score(x, y, score_value):
    score = font.render(str(score_value) + '%', True, GREEN)
    screen.blit(score, (x, y))

def error_too_close(x, y):
    global allow_drawing
    allow_drawing = False
    error_text = error_font.render('Too close to dot!', True, WHITE)
    restart_text = font.render('Press \'R\' to try again!', True, WHITE)
    screen.blit(error_text, (x, y))
    screen.blit(restart_text, (x+64, y+64))

def error_too_slow(x, y):
    global allow_drawing
    allow_drawing = False
    error_text = error_font.render('Too slow!', True, WHITE)
    restart_text = font.render('Press \'R\' to try again!', True, WHITE)
    screen.blit(restart_text, (x-10, y+64))
    screen.blit(error_text, (x, y))

def error_draw_full_circle(x, y):
    global allow_drawing
    allow_drawing = False
    error_text = error_font.render('Draw a full circle!', True, WHITE)
    restart_text = font.render('Press \'R\' to try again!', True, WHITE)
    screen.blit(restart_text, (x+64, y+64))
    screen.blit(error_text, (x, y))

def game_over_func(x, y, score_val):
    global allow_drawing
    surface.fill((0, 0, 0))
    allow_drawing = False
    if score_val >= 80.0:
        error_text = error_font.render('You did a great job!', True, GREEN)
    else:
        error_text = error_font.render('You can do better!', True, YELLOW)
    restart_text = font.render('Press \'R\' to play one more time!', True, GREEN)
    screen.blit(restart_text, (x+64, y+64))
    screen.blit(error_text, (x, y))

def restart_game():
    screen.fill((0, 0, 0))
    surface.fill((0, 0, 0))
    global drawing, last_pos, main_dot, total_sum, count, game_over, angle, arc_length, rad_sum, is_error, allow_drawing, score_val
    drawing = False
    last_pos = None
    main_dot = None
    total_sum = 0
    count = 0
    game_over = False
    angle = 0
    arc_length = 0
    rad_sum = 0
    is_error = False
    allow_drawing = True
    score_val = 0.00

running = True
while running:
    #To update percentage
    screen.blit(surface, (368, 358))
    #Drawing a dot
    pygame.draw.circle(
        screen,
        RED,
        [400, 400],
        5,
    )
    #Drawing a circle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and allow_drawing == True:
            drawing = True
            last_pos = pygame.mouse.get_pos()
            main_dot = pygame.mouse.get_pos()
            main_dot_val = math.sqrt(math.pow(main_dot[0] - 400, 2) + math.pow(main_dot[1] - 400, 2))
            start = time.time()
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if angle > 0  and angle < 2 * math.pi and is_error == False:
                error_draw_full_circle(150, 250)
                game_over = True
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = pygame.mouse.get_pos()
                pygame.draw.line(screen, color_of_line(main_dot, current_pos), last_pos, current_pos, 5)
                
                #calculate the arc length 
                arc = math.sqrt((current_pos[0] - last_pos[0]) ** 2 +(current_pos[1] - last_pos[1]) ** 2)
                arc_length += arc

                #calculate score and rad
                current_pos_val = math.sqrt(math.pow(current_pos[0] - 400, 2) + math.pow(current_pos[1] - 400, 2))
                total_sum += (current_pos_val - main_dot_val) ** 2
                count += 1
                rad_sum += current_pos_val

                #Counting percentage
                score_val = count_score(total_sum, count, main_dot_val)
                
                last_pos = current_pos

                #calculate the angle
                angle = arc_length / (rad_sum / count)
                
                #Too close error
                if current_pos_val <= 35:
                    error_too_close(150, 250)
                    drawing = False
                    is_error = True
                    game_over = True
                
                #Too slow error
                end = time.time()
                if end - start >= 20:
                    error_too_slow(250, 250)
                    drawing = False
                    is_error = True
                    game_over = True

                if angle > 2 * math.pi:
                    drawing = False
                    game_over = True
                    game_over_func(100, 100, score_val)
    
    surface.fill((0, 0, 0))  # Update percentage
    show_score(textX, textY, score_val)
    pygame.display.flip()

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restart_game()

pygame.quit()