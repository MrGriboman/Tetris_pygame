import pygame as pg
import math
import sys
import random
from settings import *
from tetromino import Tetromino
from Block import Block
from shapes import shapes
import resource
import faulthandler


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


def draw_grid():
    for x in range(0, SCREEN_WIDTH - INFO_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, BLACK, rect, 1)


def update_field(tetromino):
        for block in tetromino.blocks:
           game_field[(block.x, block.y)] = Block(block.x, block.y, tetromino.color)


def render_all_blocks():
    for block in game_field.values():
        block.render(screen)


def check_full_lines():
    count = 0
    upper_line = -1
    for i in range(20):
        line = [game_field[i][j] for j in range(10)]
        if all(line):
            count += 1
            if upper_line == -1:
                upper_line = i
            for j in range(10):
                game_field[i][j] = None
    if count > 0:        
        for i in range(upper_line - 1, 0, -1):
            for j in range(10):
                if game_field[i][j] is not None:
                    game_field[i + count][j] = game_field[i][j]
                    game_field[i + count][j].y += count
                    game_field[i][j] = None
        pg.mixer.Sound.play(line_deleted)        


def game_over():
    return any(game_field[0])


def main():
    pg.init()    
    shape = random.choice(shapes_list)
    active_tetromino = Tetromino(shape, 3, 0)
    pg.mixer.music.play(-1)
    faulthandler.enable()
    while True:
        print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        clock.tick(60)
        screen.fill(GREY)

        if active_tetromino.is_landed:
            update_field(active_tetromino)
            shape = random.choice(shapes_list)
            active_tetromino = Tetromino(shape, 3, 0)
        active_tetromino.render(screen)
        #check_full_lines()
        render_all_blocks()
        draw_grid()        

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    active_tetromino.rotate()
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