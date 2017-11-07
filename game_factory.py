import random
from game import SquareStatus, Game, GameStatus
from flask import current_app

MINIMUM = current_app.config['GAME_MINIMUM']
MAXIMUM = current_app.config['GAME_MAXIMUM']


class GameFactory:
    """
    Responsible for generating a new game and planting mines randomly
    """

    @classmethod
    def generate_new_game(cls, width, height, mines):
        """
        Generate a new game
        :param width: width of the game board
        :param height: height of the game board
        :param mines: number of mines
        :return: Game object
        """

        # validate input
        if width < MINIMUM['width'] or height < MINIMUM['height'] or mines < MINIMUM['mines']:
            width = MINIMUM['width']
            height = MINIMUM['height']
            mines = MINIMUM['mines']
        if width > MAXIMUM['width'] or height > MAXIMUM['height'] or mines > MAXIMUM['mines']:
            width = MAXIMUM['width']
            height = MAXIMUM['height']
            mines = MAXIMUM['mines']

        board = [[{'v': 0, 's': SquareStatus.CLOSED} for _ in range(width)] for _ in range(height)]

        # plant mines randomly
        planted_mines = 0
        while planted_mines < mines:
            x = random.randrange(height)
            y = random.randrange(width)
            if board[x][y]['v'] != -1:
                board[x][y]['v'] = -1
                planted_mines += 1

        # count number of surrounding mines for each square
        for x in range(height):
            for y in range(width):
                if board[x][y]['v'] == -1:
                    for (i, j) in [(a + x, b + y) for a in range(-1, 2) for b in range(-1, 2)
                                   if (0 <= a + x < height and 0 <= b + y < width)]:
                        if board[i][j]['v'] != -1:
                            board[i][j]['v'] += 1

        data = {
            'board': board,
            'width': width,
            'height': height,
            'mines': mines,
            'status': GameStatus.PLAYING,
            'flags': mines
        }

        return Game(data)


