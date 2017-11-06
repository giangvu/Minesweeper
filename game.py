from enum import Enum


class GameStatus(Enum):
    WON = 1
    PLAYING = 0
    LOST = -1


class SquareStatus(Enum):
    CLOSED = 0
    OPENED = 1
    FLAGGED = 2
    MINE_EXPLODED = 3
    WRONG_FLAGGED = 4


class Square(object):
    """
    Represent a square which is inside a game board
    """
    def __init__(self, value, status):
        """
        :param value: -1 if mine. 0 to 8 are the number of surrounding mines
        :param status: 
        """
        if value < -1 or value > 8:
            raise Exception("Invalid value")
        self.__value = value
        self.__status = SquareStatus(status)

    @property
    def value(self):
        return self.__value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    def to_json(self):
        return {'v': self.__value, 's': self.__status.value}


class Game(object):
    """
    Represent the game and control game's logic
    """

    def __init__(self, data):
        """
        Populate game's state
        """

        self.__status = GameStatus(data['status'])
        self.__flags = data['flags']
        self.__mines = data['mines']
        self.__width = data['width']
        self.__height = data['height']
        self.__board = [[0 for _ in range(self.__width)] for _ in range(self.__height)]

        for x in range(0, self.__height):
            for y in range(0, self.__width):
                item = data['board'][x][y]
                self.__board[x][y] = Square(item['v'], item['s'])

    def open(self, x, y):
        """
        Open a square inside game board
        :param x: x position
        :param y: y position
        """

        item = self.__board[x][y]
        if item.status != SquareStatus.CLOSED:
            return

        item.status = SquareStatus.OPENED

        if item.value == 0:
            self.__open_adjacent_squares(x, y)

        if item.value == -1:
            item.status = SquareStatus.MINE_EXPLODED
            self.__status = GameStatus.LOST

        self.__is_finished()

    def flag(self, x, y):
        """
        Add flag if square is closed, remove flag if square is flagged 
        :param x: x position
        :param y: y position
        """

        item = self.__board[x][y]

        if item.status not in {SquareStatus.CLOSED, SquareStatus.FLAGGED}:
            return

        item.status = SquareStatus.FLAGGED if item.status == SquareStatus.CLOSED else SquareStatus.CLOSED
        self.__flags += 1 if item.status == SquareStatus.CLOSED else -1

        self.__is_finished()

    def double_open(self, x, y):
        """
        Open all adjacent squares if the number of surrounding flags is equal to its value 
        :param x: x position
        :param y: y position
        """

        item = self.__board[x][y]

        if item.status == SquareStatus.OPENED and item.value > 0:
            positions = self.__get_adjacent_positions(x, y)

            # count flagged around
            flags = 0
            for (i, j) in positions:
                flags += 1 if self.__board[i][j].status == SquareStatus.FLAGGED else 0

            # if flagged around = number of mines around, open all unopened/non-flagged items around
            if flags == item.value:
                for (i, j) in positions:
                    self.open(i, j)

    def to_json(self, is_view=False):
        """
        Get current game state as json object
        :param is_view: True if the data is used for displaying, for database storing otherwise 
        :return: game object as json
        """

        board = [[0 for _ in range(self.__width)] for _ in range(self.__height)]
        for x in range(0, self.__height):
            for y in range(0, self.__width):
                if is_view:
                    board[x][y] = self.__to_view_data(x, y)
                else:
                    board[x][y] = self.__board[x][y].to_json()

        return {
            'board': board,
            'width': self.__width,
            'height': self.__height,
            'mines': self.__mines,
            'flags': self.__flags,
            'status': self.__status.value
        }

    def __get_adjacent_positions(self, x, y):
        """
        Get position of all adjacent squares of the square at position (x, y)
        :param x: x position
        :param y: y position
        :return: valid positions
        """

        positions = [(i + x, j + y) for i in range(-1, 2) for j in range(-1, 2)
                     if 0 <= x + i < self.__height and 0 <= y + j < self.__width]

        return positions

    def __open_adjacent_squares(self, x, y):
        """
        Open all adjacent non-mine squares of a zero square recursively
        :param x: x position
        :param y: y position
        """

        for (i, j) in self.__get_adjacent_positions(x, y):
            item = self.__board[i][j]

            if item.value != -1 and item.status == SquareStatus.CLOSED:
                item.status = SquareStatus.OPENED
                if item.value == 0:
                    self.__open_adjacent_squares(i, j)

    def __is_finished(self):
        """
        Check if the game is finished or not
        """

        opened_or_flagged = 0
        correct_flagged = 0

        for x in range(self.__height):
            for y in range(self.__width):
                item = self.__board[x][y]

                # if lost, open every unopened mines
                if self.__status == GameStatus.LOST:
                    if item.value == -1 and item.status == SquareStatus.CLOSED:
                        item.status = SquareStatus.OPENED
                    if item.value != -1 and item.status == SquareStatus.FLAGGED:
                        item.status = SquareStatus.WRONG_FLAGGED

                # count the correct flagged around item
                elif item.status in {SquareStatus.OPENED, SquareStatus.FLAGGED}:
                    opened_or_flagged += 1
                    if item.value == -1 and item.status == SquareStatus.FLAGGED:
                        correct_flagged += 1

        # if all items are opened or flagged and flagged correct = mines, user won the game
        if opened_or_flagged == self.__height * self.__width and correct_flagged == self.__mines:
            self.__status == GameStatus.WON

    def __to_view_data(self, x, y):
        """
        Convert square's status and value to corresponding number in view
        :param x: x position
        :param y: y position
        """

        square = self.__board[x][y]
        if square.status == SquareStatus.MINE_EXPLODED:
            return 9
        if square.status == SquareStatus.WRONG_FLAGGED:
            return 10
        if square.status == SquareStatus.FLAGGED:
            return 11
        if square.status == SquareStatus.CLOSED:
            return 12
        if square.status == SquareStatus.OPENED and square.value == -1:
            return 13
        return square.value



