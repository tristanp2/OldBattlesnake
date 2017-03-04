import search


class Snake:
    def __init__(self, _id, _height, _width):
        self._id = _id
        self._length = 10 #TODO: ?
        self._health = 100
        self._grid = search.SquareGrid(_height, _width)

    def gather_food(self, food, blockades):
        move = search.get_move(self._grid, self.head, food)
        return move

    def on_offense(self):
        pass

    def on_defense(self):
        pass

    def health(self):
        return self._health

    def myid(self):
        return self._id

    def status(self):
        return self._health / self._length

    def length(self):
        return self._length

    @property
    def head(self):
        return self._position

    @head.setter
    def head(self, pos):
        self._position = pos

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn
