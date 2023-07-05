import pygame as pg
import math
import sys
from settings import *
from tetromino import Tetromino

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_grid():
    for x in range(0, SCREEN_WIDTH - INFO_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, WHITE, rect, 1)

def main():
    while True:
        draw_grid()  
        tetromino = Tetromino("S")
        
        # TODO перенести в отдельный метод класса Tetromino 
        for (index, block) in enumerate(tetromino.blocks):
            if block == 1:
                rect = pg.Rect(40 + ((index - 4 * (index // 4)) - 1) * BLOCK_SIZE, 40 + (index // 4) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pg.draw.rect(screen, (255, 0, 0), rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()


if __name__ == "__main__":
    main()