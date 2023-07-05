from shapes import shapes

class Tetromino:
    def __init__(self, shape):
        self.blocks = shapes.get(shape)
