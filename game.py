from enum import Enum
import random

class GameStatus(Enum):
    WIN = 1
    PLAYING = 0
    LOST = -1

class Game:

    def __init__(self, width, height, mines):
        self.status = GameStatus.PLAYING
        self.mines = mines

class Board:

    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.items = self._create_items()
        self.mines = mines
        pass

class Item:

    def __init__(self, x, y):
        self.x = x
        self.y = y
