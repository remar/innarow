import json

class Game:
    def __init__(self, player1 = None, player2 = None, moves = None) -> None:
        self.player1 = player1
        self.player2 = player2
        self.moves = moves or []

    def move(self, player, x, y):
        if self.player1 == None or self.player2 == None:
            raise PlayersMissingError
        if not self.__players_turn(player):
            raise NotPlayersTurnError
        self.moves.append([x, y])

    def to_json(self):
        return json.dumps({"player1":self.player1, "player2":self.player2, "moves":self.moves})

    def __players_turn(self, player):
        return self.__current_turn() == player

    def __current_turn(self):
        return self.player1 if len(self.moves) % 2 == 0 else self.player2

class PlayersMissingError(Exception): pass
class NotPlayersTurnError(Exception): pass
