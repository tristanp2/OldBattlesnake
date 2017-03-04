
class Snake:
    def __init__(self, _id, position, turn):
        self._id = _id
        self._position = position
        self._turn = turn

    def health(self):
        return self._health

    def id(self):
        return self.id
    
    def current(self):
        return self._position

    def turn(self):
        return self._turn

