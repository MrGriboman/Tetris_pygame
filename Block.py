import pygame as pg
from settings import *

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def render(self, screen, color):
        rect = pg.Rect(self.get_x(), self.get_y(), BLOCK_SIZE, BLOCK_SIZE)
        pg.draw.rect(screen, color, rect)

    
    def get_x(self):
        return self.x * BLOCK_SIZE


    def get_y(self):
        return self.y * BLOCK_SIZE