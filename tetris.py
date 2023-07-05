import pygame as pg
import math
import sys
from settings import *
from tetromino import Tetromino
from Block import Block

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_grid():
    for x in range(0, SCREEN_WIDTH - INFO_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, WHITE, rect, 1)

def main():
    pg.init()
    tetrominoes = []
    tetromino = Tetromino("I", 3, 3)
    tetrominoes.append(tetromino)
    while True:
        screen.fill(BLACK)
        for figure in tetrominoes:
            figure.render(screen)
        draw_grid()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    tetromino.rotate()
                if event.key == pg.K_DOWN:
                    tetromino.go_down()
                if event.key == pg.K_LEFT:
                    tetromino.go_left()
                if event.key == pg.K_RIGHT:
                    tetromino.go_right()
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()


if __name__ == "__main__":
    main()