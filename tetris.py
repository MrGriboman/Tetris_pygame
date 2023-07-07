import pygame as pg
import math
import sys
import random
from settings import *
from tetromino import Tetromino
from Block import Block
from shapes import shapes


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
move_piece_down_event = pg.USEREVENT + 1

pg.time.set_timer(move_piece_down_event, MOVE_DOWN_TIMER)

tetrominoes = []
game_field = [[None] * 10 for i in range(20)]
shapes_list = list(shapes.keys())


def draw_grid():
    for x in range(0, SCREEN_WIDTH - INFO_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, BLACK, rect, 1)


def update_field(tetromino):
        for block in tetromino.blocks:
            game_field[block.y][block.x] = Block(block.x, block.y, tetromino.color)


def render_all_blocks():
    for i in range(20):
        for j in range(10):
            if game_field[i][j] is not None:
                game_field[i][j].render(screen)

def check_full_lines():
    deleted = False
    for i in range(20):
        line = [game_field[i][j] for j in range(10)]
        if all(line):
            deleted = True
            for j in range(10):
                game_field[i][j] = None
    '''if deleted:
        for i in range(20):
            for j in range(10):
                if game_field[i][j][0] == 1:
                    k = i
                    color = game_field[i][j][1]
                    while k < 19 and game_field[k + 1][j][0] == 0:
                        game_field[k][j] == (0, None)
                        game_field[k + 1][j] = (1, color)
                        k += 1'''


def main():
    pg.init()    
    shape = random.choice(shapes_list)
    active_tetromino = Tetromino(shape, 3, 0)    
    while True:
        clock.tick(60)
        screen.fill(GREY)

        if active_tetromino.is_landed:
            update_field(active_tetromino)
            shape = random.choice(shapes_list)
            active_tetromino = Tetromino(shape, 3, 0)
        active_tetromino.render(screen)
        check_full_lines()
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