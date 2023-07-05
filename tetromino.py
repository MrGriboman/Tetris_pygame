from shapes import shapes, pivots
import pygame as pg
from settings import *
from Block import Block

class Tetromino:
    def __init__(self, shape, x, y):
        self.blocks_coords = shapes.get(shape)
        self.x = x
        self.y = y
        self.shape = shape
        self.blocks = []
        self.fill_blocks()


    def fill_blocks(self):
        for (index, block) in enumerate(self.blocks_coords):
            if block == 1:
                block_x = self.x + ((index - 4 * (index // 4)) - 1)
                block_y = self.y + (index // 4)
                self.blocks.append(Block(block_x, block_y))


    def render(self, screen):
        for block in self.blocks:
            block.render(screen, RED)

    def rotate(self):
        if self.shape == "O":
            return
        pivot = pivots.get(self.shape)
        pivot_x = self.x + ((pivot - 4 * (pivot // 4)) - 1)
        pivot_y = self.y + (pivot // 4)
        for block in self.blocks:
            block.x -= pivot_x
            block.y -= pivot_y
            block.x, block.y = block.y, -block.x
            block.x += pivot_x
            block.y += pivot_y


    def go_down(self):
        self.y += 1
        for block in self.blocks:
            block.y += 1


    def go_left(self):
        self.x -= 1
        for block in self.blocks:
            block.x -= 1


    def go_right(self):
        self.x += 1
        for block in self.blocks:
            block.x += 1
