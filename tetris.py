import pygame as pg
import pygame.freetype
import math
import sys
import random
import copy
from settings import *
from tetromino import Tetromino
from Block import Block
from shapes import shapes

pg.init()   
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
move_piece_down_event = pg.USEREVENT + 1

pg.time.set_timer(move_piece_down_event, MOVE_DOWN_TIMER)

tetrominoes = []
game_field = dict()
shapes_list = list(shapes.keys())

pg.mixer.init()
pg.mixer.music.load('sounds/main_theme.wav')
line_deleted = pg.mixer.Sound('sounds/line_deleted.wav')
rotation = pg.mixer.Sound('sounds/click.wav')
hit_ground = pg.mixer.Sound('sounds/hit.wav')

GAME_FONT = pg.freetype.Font('font.ttf', 24)


def draw_grid():
    for x in range(0, SCREEN_WIDTH - INFO_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, BLACK, rect, 1)


def draw_next_tetromino(tetromino):
    rect = pg.Rect(450, 100, BLOCK_SIZE * 5, BLOCK_SIZE * 5)
    pg.draw.rect(screen, BLACK, rect)
    tetromino.render(screen)


def update_field(tetromino):
        for block in tetromino.blocks:
           game_field[(block.x, block.y)] = Block(block.x, block.y, tetromino.color)


def render_all_blocks():
    for block in game_field.values():
        block.render(screen)


def change_score(lines, score):
    if lines == 1:
        score += 40
    elif lines == 2:
        score += 100
    elif lines == 3:
        score += 300
    elif lines == 4:
        score += 1200
    return score


def check_full_lines(score, active_tetromino, next_tetromino):
    lines = []
    for i in range(20):
       lines.append({k: v for k, v in game_field.items() if k[1] == i})
    full_lines = [sorted(line, key=lambda x: x[0]) for line in lines if len(line) == 10]
    if full_lines:        
        pg.mixer.Sound.play(line_deleted)
        number_of_lines = len(full_lines)        
        score = change_score(number_of_lines, score)
        for i in range(10):            
            for line in full_lines:                      
                game_field.pop((i, line[0][1]))
                render_everything(score, next_tetromino)
                pg.display.flip()
            delete_time = pg.time.get_ticks() + 30
            while pg.time.get_ticks() != delete_time:
                pass                
        
        for full_line in full_lines:
            dict_items = copy.deepcopy(game_field)
            for item in sorted(dict_items.items(), key=lambda x: -x[0][1]):
                coords, block = item[0], item[1]
                new_coords = (coords[0], coords[1] + 1)
                if coords[1] < full_line[0][1] and new_coords not in game_field:
                    game_field.pop(coords)
                    game_field[new_coords] = Block(new_coords[0], new_coords[1], block.color)
    return score


def game_over():
    return any([block.y <= 0 for block in game_field.values()])


def render_score(score):
    GAME_FONT.render_to(screen, (520, 700), 'SCORE')
    GAME_FONT.render_to(screen, (550, 750), str(score))


def render_everything(score, next_tetromino):
    screen.fill(GREY)
    render_score(score)
    render_all_blocks()
    draw_grid()
    draw_next_tetromino(next_tetromino)


def main():   
    score = 0
    level = 1
    shape = random.choice(shapes_list)
    active_tetromino = Tetromino(shape, 3, 0)
    next_shape = random.choice(shapes_list)
    next_tetromino = Tetromino(next_shape, 13, 4)
    pg.mixer.music.play(-1)
    while True:
        clock.tick(60)
        if not game_over():            
            render_everything(score, next_tetromino)
            if active_tetromino.is_landed:
                update_field(active_tetromino)
                shape = random.choice(shapes_list)
                active_tetromino = Tetromino(next_tetromino.shape, 3, 0)
                next_tetromino = Tetromino(shape, 13, 4)
                render_everything(score, next_tetromino)
                pg.display.flip()
                timer = pg.time.get_ticks() + 30
                while pg.time.get_ticks() != timer:
                    pass
                score = check_full_lines(score, active_tetromino, next_tetromino)
            active_tetromino.render(screen)
        else:
            screen.fill(BLACK)
            GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2), 'GAME OVER, PRESS SPACE TO RESTART', WHITE)
            GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100), f'SCORE: {score}', WHITE)
        if not game_over():
            for event in pg.event.get():            
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        pg.mixer.Sound.play(rotation)
                        active_tetromino.rotate(game_field)
                    if event.key == pg.K_LEFT:
                        active_tetromino.go_left(game_field)
                    if event.key == pg.K_RIGHT:
                        active_tetromino.go_right(game_field)
                    if event.key == pg.K_DOWN:
                        pg.time.set_timer(move_piece_down_event, 50)
                    if event.key == pg.K_SPACE:
                        pg.mixer.Sound.play(hit_ground)
                        pg.time.set_timer(move_piece_down_event, 1)
                if event.type == move_piece_down_event:
                    if not active_tetromino.go_down(game_field):
                        active_tetromino.is_landed = True
                        pg.time.set_timer(move_piece_down_event, MOVE_DOWN_TIMER)
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE or event.key == pg.K_DOWN:
                        pg.time.set_timer(move_piece_down_event, MOVE_DOWN_TIMER)
                if event.type == pg.QUIT:
                    pg.quit()
        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        game_field.clear()
                        score = 0
                        pg.mixer.music.play(-1)
                if event.type == pg.QUIT:
                    pg.quit()
        pg.display.update()
    

if __name__ == "__main__":
    main()