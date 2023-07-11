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
                self.blocks.append(Block(block_x, block_y, self.color))


    def render(self, screen):
        for block in self.blocks:
            block.render(screen)


    def rotate(self, game_field):
        if self.shape == "O":
            return
        pivot = pivots.get(self.shape)
        pivot_x = self.x + ((pivot - 4 * (pivot // 4)) - 1)
        pivot_y = self.y + (pivot // 4)
        old_blocks = self.blocks
        new_blocks = []
        for block in self.blocks:
            x, y, = block.x, block.y
            x -= pivot_x
            y -= pivot_y
            x, y = y, -x
            x += pivot_x
            y += pivot_y
            new_blocks.append(Block(x, y, self.color))
        for block in new_blocks:
            if (block.x, block.y) in game_field:
                return
        self.blocks = new_blocks       
        while self.get_right() > RIGHT_BORDER - 1:
            can_go_left = self.go_left(game_field)
            if not can_go_left:
                self.blocks = old_blocks
                return
        while self.get_left() < LEFT_BORDER:
            can_go_right = self.go_right(game_field)
            if not can_go_right:
                self.blocks = old_blocks
                return
        while self.get_bottom() > BOTTOM_BORDER - 1:
            can_go_up = self.go_up(game_field)
            if not can_go_up:
                self.blocks = old_blocks
                return


    def go_down(self, game_field):
        if self.get_bottom() + 1 >= BOTTOM_BORDER:
            return False
        for block in self.blocks:
            if (block.x, block.y + 1) in game_field:
                return False
        for block in self.blocks:
            block.y += 1
        self.y += 1
        return True


    def go_up(self, game_field):
        if self.get_top() <= 0:
            return False
        for block in self.blocks:
            if (block.x, block.y - 1) in game_field:
                return False
        for block in self.blocks:
            block.y -= 1
        self.y -= 1
        return True


    def go_left(self, game_field):
        if self.get_left() <= LEFT_BORDER:
            return False
        for block in self.blocks:
            if (block.x - 1, block.y) in game_field:
                return False
        for block in self.blocks:
            block.x -= 1
        self.x -= 1
        return True


    def go_right(self, game_field):
        if self.get_right() + 1 >= RIGHT_BORDER:
            return False
        for block in self.blocks:
            if (block.x + 1, block.y) in game_field:
                return False
        for block in self.blocks:
            block.x += 1
        self.x += 1
        return True


    def get_bottom(self):
        return max([block.y for block in self.blocks])

    def get_top(self):
        return min([block.y for block in self.blocks])

    
    def get_left(self):
        return min([block.x for block in self.blocks])


    def get_right(self):
        return max([block.x for block in self.blocks])