import pygame as pg
import pygame.freetype
import math
import sys
import random
from settings import *
from tetromino import Tetromino
from Block import Block
from shapes import shapes
import resource
import faulthandler

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
    elif score == 3:
        score += 300
    elif score == 4:
        score += 1200
    return score


def check_full_lines(score):
    lines = []
    for i in range(20):
       lines.append({k: v for k, v in game_field.items() if k[1] == i})
    full_lines = [line for line in lines if len(line) == 10]
    if full_lines:        
        pg.mixer.Sound.play(line_deleted)
        highest_line = min([list(line.keys())[0][1] for line in full_lines])
        number_of_lines = len(full_lines)
        score = change_score(number_of_lines, score)
        for line in full_lines:
            for coords in line:
                game_field.pop(coords)
        for i in range(highest_line - 1, -1, -1):
            for j in range(10):
                x, y, = j, i
                if (x, y) not in game_field:
                    continue
                count = 0
                block = game_field.get(x, y)
                while (x, y + 1) not in game_field and count < number_of_lines:
                    y += 1
                    count += 1
                                
                game_field[(x, y)] = Block(x, y, game_field.get((j, i)).color)
                game_field.pop((j, i))
    return score


def game_over():
    return any([block.y <= 0 for block in game_field.values()])


def main():   
    score = 0  
    shape = random.choice(shapes_list)
    active_tetromino = Tetromino(shape, 3, 0)
    next_shape = random.choice(shapes_list)
    next_tetromino = Tetromino(next_shape, 13, 4)
    pg.mixer.music.play(-1)
    faulthandler.enable()
    while True:
        #print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        clock.tick(60)
        screen.fill(GREY)
        GAME_FONT.render_to(screen, (520, 700), 'SCORE')
        GAME_FONT.render_to(screen, (550, 750), str(score))

        if active_tetromino.is_landed:
            update_field(active_tetromino)
            shape = random.choice(shapes_list)
            active_tetromino = Tetromino(next_tetromino.shape, 3, 0)
            next_tetromino = Tetromino(shape, 13, 4)
        active_tetromino.render(screen)        
        score = check_full_lines(score)
        render_all_blocks()
        draw_grid()
        draw_next_tetromino(next_tetromino)      
     
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    active_tetromino.rotate(game_field)
                if event.key == pg.K_LEFT:
                    active_tetromino.go_left(game_field)
                if event.key == pg.K_RIGHT:
                    active_tetromino.go_right(game_field)
                if event.key == pg.K_DOWN:
                    pg.time.set_timer(move_piece_down_event, 1)
            if event.type == move_piece_down_event:
                if not active_tetromino.go_down(game_field):
                    active_tetromino.is_landed = True
                    pg.time.set_timer(move_piece_down_event, MOVE_DOWN_TIMER)
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    pg.time.set_timer(move_piece_down_event, MOVE_DOWN_TIMER)
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()
    

if __name__ == "__main__":
    main()