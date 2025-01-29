import sys
import random
import time
import configparser

import pygame


def run_game():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Reaction")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    config = configparser.ConfigParser()
    config.read('settings_for_game.ini')

    square_size = int(config['DEFAULT']['size'])
    squares_left = int(config['DEFAULT']['number'])
    time_value = int(config['DEFAULT']['time'])

    delay_between_squares = (time_value / 2) * 1000
    if time_value == 0:
        square_duration = 1000
    else:
        square_duration = (time_value / 2) * 1000

    hits = 0
    misses = 0
    total_squares = 0 
    
    clock = pygame.time.Clock()
    running = True
    square = None
    start_time = 0
    game_start_time = time.time()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if square is not None and square.collidepoint(mouse_pos):
                    hits += 1
                    square = None  
                else:
                    misses += 1
    
        screen.fill((0, 0, 0))
        
        if square is not None:
            pygame.draw.rect(screen, (255, 255, 255), square)
        
        current_time = pygame.time.get_ticks()
        if square is None and current_time - start_time > delay_between_squares:
            if total_squares < squares_left:
                x = random.randint(square_size, screen.get_width() - square_size)
                y = random.randint(square_size, screen.get_height() - square_size)
                square = pygame.Rect(x, y, square_size, square_size)
                start_time = current_time
                total_squares += 1
            else:
                running = False

        if square is not None and current_time - start_time > square_duration:
            square = None
    
        text_hits = font.render(f"Hits: {hits}", True, (255, 255, 255))
        text_misses = font.render(f"Miss: {misses}", True, (255, 255, 255))
        screen.blit(text_hits, (10, 10))
        screen.blit(text_misses, (10, 40))

        pygame.display.flip()
        clock.tick(60)
    
    total_time = time.time() - game_start_time

    game_over_text = "Game over!"
    final_hits = f"Hits: {hits}"
    final_misses = f"Past the target: {misses}"
    final_missed = f"Missed targets: {squares_left - hits}"
    total_time_str = f"Game time: {total_time:.2f} seconds"
    
    screen.fill((0, 0, 0))
    text_surface = font.render(game_over_text, True, (255, 255, 255))
    screen.blit(text_surface, (300, 250))

    text_surface = font.render(final_hits, True, (255, 255, 255))
    screen.blit(text_surface, (320, 280))

    text_surface = font.render(final_misses, True, (255, 255, 255))
    screen.blit(text_surface, (320, 310))

    text_surface = font.render(final_missed, True, (255, 255, 255))
    screen.blit(text_surface, (320, 340))

    text_surface = font.render(total_time_str, True, (255, 255, 255))
    screen.blit(text_surface, (320, 370))
    
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.quit()