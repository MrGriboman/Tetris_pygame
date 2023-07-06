from shapes import shapes, pivots, colors
import pygame as pg
from settings import *
from Block import Block

class Tetromino:
    def __init__(self, shape, x, y):
        self.blocks_coords = shapes.get(shape)
        self.x = x
        self.y = y
        self.shape = shape
        self.color = colors.get(shape)
        self.is_landed = False
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
            block.render(screen, self.color)

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
        if self.get_bottom() + 1 >= BOTTOM_BORDER:
            return False
        self.y += 1
        for block in self.blocks:
            block.y += 1
        return True


    def go_left(self):
        if self.get_left() <= LEFT_BORDER:
            return False
        self.x -= 1
        for block in self.blocks:
            block.x -= 1
        return True


    def go_right(self):
        if self.get_right() + 1 >= RIGHT_BORDER:
            return False
        self.x += 1
        for block in self.blocks:
            block.x += 1
        return True


    def get_bottom(self):
        return max([block.y for block in self.blocks])

    
    def get_left(self):
        return min([block.x for block in self.blocks])


    def get_right(self):
        return max([block.x for block in self.blocks])