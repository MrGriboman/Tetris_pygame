import pygame as pg
from settings import *

class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


    def render(self, screen):
        rect = pg.Rect(self.get_x(), self.get_y(), BLOCK_SIZE, BLOCK_SIZE)
        pg.draw.rect(screen, self.color, rect)

    
    def get_x(self):
        return self.x * BLOCK_SIZE


    def get_y(self):
        return self.y * BLOCK_SIZE