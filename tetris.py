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
game_field = [[0] * 10 for i in range(20)]
shapes_list = list(shapes.keys())

def draw_grid():
    for x in range(0, SCREEN_WIDTH - INFO_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, WHITE, rect, 1)


def update_field(tetromino):
        for block in tetromino.blocks:
            game_field[block.y][block.x] = 1
        print(game_field)


def main():
    pg.init()    
    shape = random.choice(shapes_list)
    active_tetromino = Tetromino(shape, 3, 0)
    tetrominoes.append(active_tetromino)

    while True:
        clock.tick(60)
        screen.fill(BLACK)
        if tetrominoes[-1].is_landed:
            update_field(active_tetromino)
            shape = random.choice(shapes_list)
            active_tetromino = Tetromino(shape, 3, 0)
            tetrominoes.append(active_tetromino)
        for figure in tetrominoes:
            figure.render(screen)
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
                    MOVE_DOWN_TIMER = 600
            if event.type == move_piece_down_event:
                active_tetromino.is_landed = not active_tetromino.go_down(game_field)
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    MOVE_DOWN_TIMER = 800
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()
    

if __name__ == "__main__":
    main()